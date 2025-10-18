import pandas as pd

def convert_amounts_to_float(df: pd.DataFrame) -> pd.DataFrame:
    """Convert 'amount' and 'balance' columns to floats, handling commas and NaNs."""
    for col in ['amount', 'balance']:
        df[col] = df[col].astype(str).str.replace(',', '.').replace('nan', None)
        df[col] = df[col].astype(float)
    return df

def convert_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Convert 'date' column to datetime, safely."""
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def extract_missing_counterparty_names(df: pd.DataFrame) -> pd.DataFrame:
    """Extract counterparty_name from 'description' if both counterparty_name and account_number are missing."""
    mask = df['counterparty_name'].isna() & df['counterparty_account_number'].isna()
    extracted_names = df.loc[mask, 'description'].str.extract(
        r'(?:TIME|UUR)\s+(.*?)\s+(?:BE|NL|LUL|FR|DE|ES|PL|\d{4} IEDUBLIN)', expand=False
    )
    df.loc[mask, 'counterparty_name'] = extracted_names
    return df

def set_counterparty_name_for_deposits(df: pd.DataFrame) -> pd.DataFrame:
    """Set counterparty_name to 'Cash deposit' for deposits in multiple languages."""
    deposit_prefixes = ("DEPOSIT", "STORTING")  # English + Dutch
    mask_deposit = df['description'].str.startswith(deposit_prefixes, na=False)
    df.loc[mask_deposit & df['counterparty_name'].isna(), 'counterparty_name'] = "Cash deposit"
    return df

def extract_iban_for_savings(df: pd.DataFrame) -> pd.DataFrame:
    """Extract IBAN from description for automatic savings and assign to counterparty_account_number.
    Handles both English and Dutch descriptions.
    """
    # Handle both English and Dutch prefixes
    savings_prefixes = ("AUTOMATIC SAVINGS", "AUTOMATISCH SPAREN")
    mask_savings = df['description'].str.startswith(savings_prefixes, na=False)
    
    # Extract BE IBAN
    extracted_iban = df.loc[mask_savings, 'description'].str.extract(
        r'(BE\d{2}\s\d{4}\s\d{4}\s\d{4})', expand=False
    )
    df.loc[mask_savings, 'counterparty_account_number'] = extracted_iban
    return df

def set_counterparty_name_for_mobile_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Set counterparty_name to 'Payconiq' for mobile payments in multiple languages."""
    mobile_prefixes = ("MOBILE PAYMENT", "MOBIELE BETALING")  # English + Dutch
    mask_mobile = df['description'].str.startswith(mobile_prefixes, na=False)
    df.loc[mask_mobile, 'counterparty_name'] = "Payconiq"
    return df

def ensure_text_columns_are_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Convert selected text columns to string type."""
    text_columns = ['account_number', 'currency', 'description', 
                    'counterparty_account_number', 'counterparty_name']
    for col in text_columns:
        df[col] = df[col].astype(str)
    return df

def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run all data cleaning and transformations in order."""
    df = convert_amounts_to_float(df)
    df = convert_date_column(df)
    df = extract_missing_counterparty_names(df)
    df = set_counterparty_name_for_deposits(df)
    df = extract_iban_for_savings(df)
    df = set_counterparty_name_for_mobile_payments(df)
    df = ensure_text_columns_are_strings(df)
    return df
