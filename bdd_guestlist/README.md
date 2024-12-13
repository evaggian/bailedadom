# Export party guestlist from stripe

This script processes a CSV file containing payment information, filters specific columns, calculates ticket quantities, adds an index, and saves the output as an CSV file with a total sum row.

## Requirements

- Python 3.x
- pandas

## Usage

```bash
python export_from_stripe.py <date> [<input_csv> <output_csv> <extra_names>] [-r | report]
```

Replace <date> with the specific party date in DD-MM-YYYY format.
Optionally, provide <input_csv> as the path to your input CSV file and <output_csv> as the desired path for the output CSV file.
Optionally, provide <extra_names> as a comma-separated list of additional names (e.g., "Guest1,Guest2").

Including Financial Details
Use the "- flag or <report> keyword to include financial columns (Amount, Fee, Net Income) in the exported CSV. If this option is omitted, financial details will be excluded from the output.

## Tests

Run unit tests using:
```bash
python -m unittest discover
```
