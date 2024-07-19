import pandas as pd
import sys

def filter_csv(input_csv, output_csv, specified_date):
    # Load the CSV file into a DataFrame and clean data
    df = pd.read_csv(input_csv)
    df['Amount'] = pd.to_numeric(df['Amount'].replace('[\$,]', '', regex=True), errors='coerce').fillna(0).astype(int)
    df['Date'] = pd.to_datetime(df['Created date (UTC)']).dt.date  # Directly convert and rename date column
    df.rename(columns={'Checkout Custom Field 1 Value': 'Name'}, inplace=True)

    # Define columns to keep and ensure they exist in the DataFrame
    columns_to_keep = ['Date', 'Amount', 'Customer Email', 'Name']
    if any(col not in df.columns for col in columns_to_keep):
        raise ValueError(f"Missing columns in the CSV file: {', '.join([col for col in columns_to_keep if col not in df.columns])}")

    # Filter and keep the specified columns only
    filtered_df = df[columns_to_keep]

    # Function to determine ticket quantity based on 'Amount' and 'Date'
    def calculate_tickets(row):
        mapping = {(1500, specified_date): 1, (3000, specified_date): 2, (4500, specified_date): 3}
        default_mapping = {1000: 1, 2000: 2, 3000: 3}

        return mapping.get((row['Amount'], row['Date'].isoformat()), default_mapping.get(row['Amount'], 0))

    # Apply function to create new column for tickets quantity
    filtered_df['Tickets quantity'] = filtered_df.apply(calculate_tickets, axis=1)

    # Remove rows where 'Tickets quantity' is 0
    filtered_df = filtered_df[filtered_df['Tickets quantity'] != 0]

    # Sort and reorder the DataFrame for the output
    filtered_df = filtered_df.sort_values(by='Name')[['Name', 'Tickets quantity', 'Customer Email', 'Date']]

    # Add an index column starting from 1
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1
    filtered_df.index.name = 'Index'

    # Calculate the sum of the 'Tickets quantity' column
    total_tickets = filtered_df['Tickets quantity'].sum()

    # Add an index column starting from 1
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1
    filtered_df.index.name = 'Index'

    # Create a new row for the total sum
    total_row = pd.DataFrame([['Total', total_tickets, '', '']], columns=filtered_df.columns, index=[filtered_df.index.max() + 1])

    # Append the total row to the DataFrame
    filtered_df = pd.concat([filtered_df, total_row])

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=True)
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
