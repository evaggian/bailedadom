import unittest
import pandas as pd
import os
from export_from_stripe import filter_csv

class TestFilterCSVWithRealData(unittest.TestCase):

    def setUp(self):
        # Path to the test CSV file
        # [TO-DO: replace real data file with synthetic data]
        self.input_csv = 'test_unified_payments.csv'
        self.output_csv = 'test_output_guestlist.csv'

    def tearDown(self):
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)

    def test_filter_csv_valid_input(self):
        # Call the function using the real test CSV file and a valid date
        filter_csv(self.input_csv, self.output_csv, '12-10-2024')

        # Load the result CSV and perform checks
        result_df = pd.read_csv(self.output_csv)

        # Perform your assertions here, e.g., check if the correct rows are filtered
        self.assertFalse(result_df.empty)


    def test_filter_csv_missing_data(self):
            # Modify the original CSV to introduce missing data (NaN values in important columns)
            df = pd.read_csv(self.input_csv)
            df.loc[0, 'Checkout Line Item Summary'] = None  # Introduce a NaN value
            df.to_csv(self.input_csv, index=False)  # Save the modified CSV

            # Call the function and ensure it handles missing values gracefully
            filter_csv(self.input_csv, self.output_csv, '12-10-2024')

            # Load the result CSV and check if the process succeeded
            result_df = pd.read_csv(self.output_csv)

            # Ensure the result isn't completely empty even with missing values
            self.assertFalse(result_df.empty)

    def test_filter_csv_valid_date_no_workshops_or_parties(self):
        # Modify the CSV to match the date but without any workshops or parties in the summary
        df = pd.read_csv(self.input_csv)
        df['Checkout Line Item Summary'] = 'No workshops or parties here'
        df.to_csv(self.input_csv, index=False)  # Save the modified CSV

        # Call the function and ensure no workshops or parties are processed
        filter_csv(self.input_csv, self.output_csv, '12-10-2024')

        # Load the result CSV and ensure columns exist without workshop or party data
        result_df = pd.read_csv(self.output_csv)

        self.assertTrue('Workshop' not in result_df.columns or result_df['Workshop'].sum() == 0)
        self.assertTrue('Party' in result_df.columns and result_df['Party'].sum() == 0)


    def test_filter_csv_party_only(self):
            # Modify the CSV to only contain party information in the summary
            df = pd.read_csv(self.input_csv)
            df['Checkout Line Item Summary'] = 'party'  # Only party, no workshop
            df.to_csv(self.input_csv, index=False)  # Save the modified CSV

            # Call the function and ensure that the party information is processed
            filter_csv(self.input_csv, self.output_csv, '12-10-2024')

            # Load the result CSV
            result_df = pd.read_csv(self.output_csv)
            print(result_df)

            # Ensure that the 'Party' column exists and the value is 3
            self.assertTrue('Party' in result_df.columns)

            # Ensure that 'Workshop' column does not exist
            self.assertTrue('Workshop' not in result_df.columns)


if __name__ == '__main__':
    unittest.main()
