import pandas as pd
import sys
import re

def filter_csv(input_csv, output_csv, specified_date, include_financials, extra_names=None):

    # Load the CSV file into a DataFrame and clean data
    df = pd.read_csv(input_csv)

    # Convert 'Amount' and 'Fee' to numeric (float), handling commas as decimal separators
    df['Amount'] = pd.to_numeric(df['Amount'].str.replace(',', '.'), errors='coerce').fillna(0.0)

    # Check if 'Fee' exists, and handle accordingly
    if 'Fee' in df.columns:
        df['Fee'] = pd.to_numeric(df['Fee'].str.replace(',', '.'), errors='coerce').fillna(0.0)
    else:
        df['Fee'] = 0.0  # Set to 0.0 if the Fee column is missing

    # Calculate Net Income as Amount - Fee
    df['Net Income'] = df['Amount'] - df['Fee']

    df['Date'] = pd.to_datetime(df['Created date (UTC)']).dt.date  # Convert and rename date column
    df.rename(columns={'Checkout Custom Field 1 Value': 'Name', 'Checkout Custom Field 2 Value': 'Workshop Level'}, inplace=True)

    # Define columns to keep and ensure they exist in the DataFrame
    columns_to_keep = ['Date', 'Amount', 'Fee', 'Net Income', 'Name', 'Workshop Level', 'Checkout Line Item Summary']
    if any(col not in df.columns for col in columns_to_keep):
        raise ValueError(f"Missing columns in the CSV file: {', '.join([col for col in columns_to_keep if col not in df.columns])}")

    # Filter and keep the specified columns only
    filtered_df = df[columns_to_keep]

    # Remove rows where 'Checkout Line Item Summary' doesn't contain the specified date in MM/DD format
    day, month, _ = specified_date.split('-')  # Extract day, month, year
    date_pattern = f"{int(day)}/{int(month)}"

    # Ensure the 'Checkout Line Item Summary' column is a string
    filtered_df['Checkout Line Item Summary'] = filtered_df['Checkout Line Item Summary'].astype(str)
    filtered_df = filtered_df[filtered_df['Checkout Line Item Summary'].str.contains(date_pattern)]

    # Create new columns 'Workshop' and 'Party' initialized to 0
    filtered_df['Workshop'] = 0
    filtered_df['Intermediate'] = 0
    filtered_df['Open level'] = 0
    filtered_df['Party'] = 0

    # Function to update the Workshop Level values and handle workshop and party quantities
    def update_workshop_party(row):
        summary = row['Checkout Line Item Summary']

        # Extract numbers associated with workshop
        workshop_match = re.search(r'(\d+)\s*workshop', summary, re.IGNORECASE)
        if workshop_match:
            quantity = int(workshop_match.group(1))
            row['Workshop'] += quantity

            # If quantity is 2, append 'both' to 'Workshop Level'
            if quantity == 2:
                row['Workshop Level'] = 'Both'
                row['Intermediate'] = 1
                row['Open level'] = 1

        # Extract the number inside parentheses for party or default to 1
        party_match = re.search(r'party.*?\((\d+)\)', summary, re.IGNORECASE)

        if party_match:
            couples_match = re.search(r'couples.*?\((\d+)\)', summary, re.IGNORECASE)
            if couples_match:
                row['Party'] += 2
            else:
                row['Party'] += int(party_match.group(1))
        elif 'party' in summary:
            row['Party'] += 1

        # Update the 'Workshop Level' column: rename specific values
        if row['Workshop Level'] == 'openlevelworkshop':
            row['Workshop Level'] = 'Open level'
            row['Open level'] = 1
        elif row['Workshop Level'] == 'intermediateworkshop':
            row['Workshop Level'] = 'Intermediate'
            row['Intermediate'] = 1

        return row

    # Apply the function to each row
    filtered_df = filtered_df.apply(update_workshop_party, axis=1)

    # Split rows where 'Name' contains multiple names separated by commas
    expanded_df = filtered_df.drop('Name', axis=1).join(
        filtered_df['Name'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('Name')
    )

    # Swap name with workshop level and increase the appropriate counter
    def swap_name_with_level(row):
        name_lower = row['Name'].strip().lower()
        if name_lower == 'intermediate':
            row['Name'], row['Workshop Level'] = row['Workshop Level'], 'Intermediate'
            row['Intermediate'] += 1
        elif name_lower == 'openlevel':
            row['Name'], row['Workshop Level'] = row['Workshop Level'], 'Open level'
            row['Open level'] += 1
        return row

    expanded_df = expanded_df.apply(swap_name_with_level, axis=1)

    # Increment 'Party' by 1 for each new row created
    #expanded_df['Party'] += 1

    # Handle additional names if provided
    if extra_names:
        extra_names_list = [name.strip() for name in extra_names.split(',')]
        # Create extra rows with the same structure as the expanded DataFrame
        extra_rows = pd.DataFrame({
            'Name': extra_names_list,
            'Workshop': 0,
            'Workshop Level': '',
            'Intermediate': 0,
            'Open level': 0,
            'Party': 1,
            'Date': '',
            'Net Income': 0,
            'Amount': 0,
            'Fee': 0
        })
        # Add the extra rows to the expanded DataFrame
        expanded_df = pd.concat([expanded_df, extra_rows], ignore_index=True)

    # Calculate the sum of 'Workshop', 'Intermediate', 'Open level', 'Party' columns
    total_workshops = expanded_df['Workshop'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_intermediate = expanded_df['Intermediate'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_open_level = expanded_df['Open level'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_parties = expanded_df['Party'].sum()

    # If the sum of 'Workshop' is 0, drop the column
    if total_workshops == 0:
        expanded_df.drop(columns=['Workshop'], inplace=True)

        # Check rows where 'Party' is 0 after dropping 'Workshop' and remove them
        expanded_df = expanded_df[expanded_df['Party'] > 0]

    # Reorder the columns to include 'Workshop Level' after 'Workshop'
    if 'Workshop' in expanded_df.columns:
        expanded_df = expanded_df[['Name', 'Workshop', 'Workshop Level', 'Intermediate', 'Open level', 'Party', 'Date', 'Amount', 'Fee', 'Net Income']]
        # Create a new row for the total sum including Workshop
        total_row = pd.DataFrame([['Total', total_workshops, '', total_intermediate, total_open_level, total_parties, '', round(expanded_df['Amount'].sum(),2), round(expanded_df['Fee'].sum(),2), round(expanded_df['Net Income'].sum(),2)]],
                                 columns=['Name', 'Workshop', 'Workshop Level', 'Intermediate', 'Open level', 'Party', 'Date', 'Amount', 'Fee', 'Net Income'],
                                 index=[expanded_df.index.max() + 1])
    else:
        expanded_df = expanded_df[['Name', 'Party', 'Date', 'Amount', 'Fee', 'Net Income']]
        # Create a new row for the total sum without Workshop
        total_row = pd.DataFrame([['Total', total_parties, '', round(expanded_df['Amount'].sum(),2), round(expanded_df['Fee'].sum(),2), round(expanded_df['Net Income'].sum(),2)]],
                                 columns=['Name', 'Party', 'Date', 'Amount', 'Fee', 'Net Income'],
                                 index=[expanded_df.index.max() + 1])

    # Capitalize the first letter of the column name
    expanded_df['Name'] = expanded_df['Name'].apply(lambda x: x.title() if isinstance(x, str) else x)


    # Sort the DataFrame by 'Name' column alphabetically
    expanded_df = expanded_df.sort_values(by='Name', ascending=True)

    # Add an empty row with the correct number of columns
    empty_row = pd.DataFrame([[None] * len(expanded_df.columns)],
                             columns=expanded_df.columns,
                             index=[expanded_df.index.max() + 1])

    # Append the empty row and total row to the DataFrame
    expanded_df = pd.concat([expanded_df, empty_row, total_row])

    if not include_financials:
        expanded_df.drop(columns=['Amount', 'Fee', 'Net Income'], inplace=True)

    # Save the filtered DataFrame to a new CSV file
    expanded_df.to_csv(output_csv, index=False)
    print(f"Filtered CSV saved as {output_csv}")

if __name__ == "__main__":
    # Default arguments
    default_input_csv = 'unified_payments.csv'
    specified_date = sys.argv[1]

    # Check for 'report' keyword to enable financials
    include_financials = '-r' in sys.argv
    args = [arg for arg in sys.argv if arg != '-r']

    # Determine optional arguments
    input_csv_path = args[2] if len(args) >= 3 and not ',' in args[2] else default_input_csv
    output_csv_path = args[3] if len(args) >= 4 and not ',' in args[3] else f'BdD_guestlist_{specified_date}.csv'
    if ',' in args[-1]:
        extra_names = args[-1]
    else:
        extra_names = None

    # Call the function
    filter_csv(input_csv_path, output_csv_path, specified_date, include_financials, extra_names)


