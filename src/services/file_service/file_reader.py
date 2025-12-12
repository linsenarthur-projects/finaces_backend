import pandas as pd

def read_csv_file(file: str) -> pd.DataFrame:
    """Read the CSV file with the proper settings."""
    column_names = [
        'Accountnumber', 'Heading', 'Name', 'Currency', 'Statement number',
        'Date', 'Description', 'Value date', 'Amount', 'Balance',
        'Credit', 'Debit', 'Counterparty account number', 'Counterparty BIC',
        'Counterparty name', 'Counterparty address', 'Standard-format reference',
        'Free-format reference'
    ]
    df = pd.read_csv(
        file,
        sep=";",
        encoding="utf-8",
        usecols=range(18),
        names=column_names,
        skiprows=1,
        na_values=["NaN"],
        parse_dates=["Date"],
        dayfirst=True,
        engine='python'
    )
    return df

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unnecessary columns from the DataFrame."""
    df = df.drop([
        'Heading', 'Name', 
        'Statement number', 
        'Value date',
        'Counterparty BIC', 
        'Counterparty address', 
        'Credit', 
        'Debit', 
        'Free-format reference',
        'Standard-format reference'
    ], axis=1)
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to a consistent format."""
    return df.rename(columns={
        'Accountnumber': 'account_number',
        'Currency': 'currency',
        'Date': 'date',
        'Description': 'description',
        'Amount': 'amount',
        'Balance': 'balance',
        'Counterparty account number': 'counterparty_account_number',
        'Counterparty name': 'counterparty_name',
        # 'Free-format reference': 'free_format_reference',
        # 'Standard-format reference': 'standard_format_reference'
    })

def upload_csv(file: str) -> pd.DataFrame:
    """Full workflow: read, clean, and rename CSV data."""
    df = read_csv_file(file)
    df = clean_dataframe(df)
    df = rename_columns(df)
    return df
