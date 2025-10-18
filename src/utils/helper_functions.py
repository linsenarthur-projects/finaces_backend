import pandas as pd

def is_new(row, existing: pd.DataFrame) -> bool:
    """Check if a row is new compared to existing accounts."""
    if pd.isna(row['iban']):
        return not ((existing['name'] == row['name']) & existing['iban'].isna()).any()
    else:
        return not ((existing['name'] == row['name']) & (existing['iban'] == row['iban'])).any()
