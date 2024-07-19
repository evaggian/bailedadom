# Export party guestlist from stripe

This script processes a CSV file containing payment information, filters specific columns, calculates ticket quantities, adds an index, and saves the output as an CSV file with a total sum row.

## Requirements

- Python 3.x
- pandas

## Usage

```bash
python export_from_stripe.py <date> [<input_csv> <output_csv>]
```

Replace <date> with the specific party date in YYYY-MM-DD format. Optionally, provide <input_csv> as the path to your input CSV file and <output_csv> as the desired path for the output CSV file.