# Export party guestlist from stripe

This script processes a CSV file containing payment information, filters specific columns, calculates ticket quantities, adds an index, and saves the output as an CSV file with a total sum row.

## Requirements

- Python 3.x
- pandas

## Usage

```bash
python export_from_stripe.py <input_csv> <output_excel> <date>
```

Replace <input_csv> with the path to your input CSV file, <output_excel> with the desired path for the output Excel file, and <date> with the specific party date in YYYY-MM-DD format.