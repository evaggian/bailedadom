import pandas as pd
import sys
import re

def filter_csv(input_csv, output_csv, specified_date):
    # Load the CSV file into a DataFrame and clean data
    df = pd.read_csv(input_csv)
    df['Amount'] = pd.to_numeric(df['Amount'].replace('[\$,]', '', regex=True), errors='coerce').fillna(0).astype(int)
    df['Date'] = pd.to_datetime(df['Created date (UTC)']).dt.date  # Directly convert and rename date column
    df.rename(columns={'Checkout Custom Field 1 Value': 'Name', 'Checkout Custom Field 2 Value': 'Workshop Level'}, inplace=True)

    # Define columns to keep and ensure they exist in the DataFrame
    columns_to_keep = ['Date', 'Amount', 'Customer Email', 'Name', 'Workshop Level', 'Checkout Line Item Summary']
    if any(col not in df.columns for col in columns_to_keep):
        raise ValueError(f"Missing columns in the CSV file: {', '.join([col for col in columns_to_keep if col not in df.columns])}")

    # Filter and keep the specified columns only
    filtered_df = df[columns_to_keep]

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

    # Calculate the sum of 'Workshop', 'Intermediate','Open level','Party' columns
    total_workshops = filtered_df['Workshop'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_intemediate = filtered_df['Intermediate'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_open_level = filtered_df['Open level'].apply(lambda x: 0 if isinstance(x, str) else x).sum()
    total_parties = filtered_df['Party'].sum()

    # If the sum of 'Workshop' is 0, drop the column
    if total_workshops == 0:
        filtered_df.drop(columns=['Workshop'], inplace=True)

    # Reorder the columns to include 'Workshop Level' after 'Workshop'
    if 'Workshop' in filtered_df.columns:
        filtered_df = filtered_df[['Name', 'Customer Email', 'Workshop', 'Workshop Level', 'Intermediate','Open level','Party', 'Date']]
        # Create a new row for the total sum including Workshop
        total_row = pd.DataFrame([['Total', '', total_workshops, '', total_intemediate, total_open_level, total_parties, '']],
                                 columns=['Name', 'Customer Email', 'Workshop', 'Workshop Level', 'Intermediate','Open level','Party', 'Date'],
                                 index=[filtered_df.index.max() + 1])
    else:
        filtered_df = filtered_df[['Name', 'Customer Email', 'Workshop Level', 'Party', 'Date']]
        # Create a new row for the total sum without Workshop
        total_row = pd.DataFrame([['Total', '', '', total_intemediate, total_open_level, total_parties, '']],
                                 columns=['Name', 'Customer Email', 'Workshop Level', 'Intermediate','Open level','Party', 'Date'],
                                 index=[filtered_df.index.max() + 1])

    # Append the total row to the DataFrame
    filtered_df = pd.concat([filtered_df, total_row])

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False)
    print(f"Filtered CSV saved as {output_csv}")

if __name__ == "__main__":
    # Default arguments
    default_input_csv = 'unified_payments.csv'
    specified_date = sys.argv[1]

    # Ensure the correct number of arguments
    if len(sys.argv) not in [2, 4]:
        print("Usage: python script.py <date> [<input_csv> <output_csv>]")
        sys.exit(1)

    input_csv_path = sys.argv[2] if len(sys.argv) == 4 else default_input_csv
    output_csv_path = sys.argv[3] if len(sys.argv) == 4 else f'BdD_guestlist_{specified_date}.csv'

    filter_csv(input_csv_path, output_csv_path, specified_date)
