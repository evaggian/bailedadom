import pandas as pd
import sys
import re

def filter_csv(input_csv, output_csv, specified_date, extra_names=None):
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
    columns_to_keep = ['Date', 'Amount', 'Fee', 'Net Income', 'Customer Email', 'Name', 'Workshop Level', 'Checkout Line Item Summary']
    if any(col not in df.columns for col in columns_to_keep):
        raise ValueError(f"Missing columns in the CSV file: {', '.join([col for col in columns_to_keep if col not in df.columns])}")

    # Filter and keep the specified columns only
    filtered_df = df[columns_to_keep]

    # Remove rows where 'Checkout Line Item Summary' doesn't contain the specified date in MM/DD format
    date_pattern = specified_date.replace('-', '/')[0:5]  # Convert specified_date to MM/DD format

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
        party_match = re.search(r'party.*\((\d+)\)', summary, re.IGNORECASE)
        if party_match:
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

    # Increment 'Party' by 1 for each new row created
    #expanded_df['Party'] += 1

    # Handle additional names if provided
    if extra_names:
        extra_names_list = [name.strip() for name in extra_names.split(',')]
        # Create extra rows with the same structure as the expanded DataFrame
        extra_rows = pd.DataFrame({
            'Name': extra_names_list,
            'Customer Email': '',
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
        expanded_df = expanded_df[['Name', 'Customer Email', 'Workshop', 'Workshop Level', 'Intermediate', 'Open level', 'Party', 'Date', 'Amount', 'Fee', 'Net Income']]
        # Create a new row for the total sum including Workshop
        total_row = pd.DataFrame([['Total', '', total_workshops, '', total_intermediate, total_open_level, total_parties, '', expanded_df['Amount'].sum(), expanded_df['Fee'].sum(), expanded_df['Net Income'].sum()]],
                                 columns=['Name', 'Customer Email', 'Workshop', 'Workshop Level', 'Intermediate', 'Open level', 'Party', 'Date', 'Amount', 'Fee', 'Net Income'],
                                 index=[expanded_df.index.max() + 1])
    else:
        expanded_df = expanded_df[['Name', 'Customer Email', 'Party', 'Date', 'Amount', 'Fee', 'Net Income']]
        # Create a new row for the total sum without Workshop
        total_row = pd.DataFrame([['Total', '', total_parties, '', expanded_df['Amount'].sum(), expanded_df['Fee'].sum(), expanded_df['Net Income'].sum()]],
                                 columns=['Name', 'Customer Email', 'Party', 'Date', 'Amount', 'Fee', 'Net Income'],
                                 index=[expanded_df.index.max() + 1])

    # Sort the DataFrame by 'Name' column alphabetically
    expanded_df = expanded_df.sort_values(by='Name', ascending=True)

    # Add an empty row with the correct number of columns
    empty_row = pd.DataFrame([[None] * len(expanded_df.columns)],
                             columns=expanded_df.columns,
                             index=[expanded_df.index.max() + 1])

    # Append the empty row and total row to the DataFrame
    expanded_df = pd.concat([expanded_df, empty_row, total_row])

    # Save the filtered DataFrame to a new CSV file
    expanded_df.to_csv(output_csv, index=False)
    print(f"Filtered CSV saved as {output_csv}")

if __name__ == "__main__":
    # Default arguments
    default_input_csv = 'unified_payments.csv'
    specified_date = sys.argv[1]

    # Determine optional arguments based on their count
    input_csv_path = sys.argv[2] if len(sys.argv) >= 3 and not ',' in sys.argv[2] else default_input_csv
    output_csv_path = sys.argv[3] if len(sys.argv) >= 4 and not ',' in sys.argv[3] else f'BdD_guestlist_{specified_date}.csv'
    extra_names = sys.argv[-1] if ',' in sys.argv[-1] else None

    filter_csv(input_csv_path, output_csv_path, specified_date, extra_names)
