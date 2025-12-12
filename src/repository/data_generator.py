import pandas as pd
from datetime import date

# ----------------------------
# Accounts / Internal Accounts
# ----------------------------
def get_internal_accounts() -> pd.DataFrame:
    """Return DataFrame of internal accounts."""
    return pd.DataFrame([
        {'iban': 'BE76 7340 4232 9795', 'name': 'Zichtrekening', 'type': 'internal'},
        {'iban': 'BE31 7450 2762 4255', 'name': 'Spaarrekening', 'type': 'internal'},
        {'iban': 'BE98 7410 2384 6393', 'name': 'Start2Safe', 'type': 'internal'},
    ])


def get_accounts_from_data(df: pd.DataFrame, internal_accounts: pd.DataFrame) -> pd.DataFrame:
    """Extract unique accounts from transaction DataFrame, 
    marking them as internal if IBAN is in internal_accounts."""

    accounts = df[['counterparty_account_number', 'counterparty_name']].copy()
    accounts.columns = ['iban', 'name']
    accounts.drop_duplicates(subset=['iban'], inplace=True)
    accounts.reset_index(drop=True, inplace=True)

    # Add type column
    accounts['type'] = 'external'

    # Mark as internal if IBAN is in internal_accounts
    internal_ibans = set(internal_accounts['iban'])
    accounts.loc[accounts['iban'].isin(internal_ibans), 'type'] = 'internal'

    return accounts


# ----------------------------
# Categories
# ----------------------------
def get_categories() -> pd.DataFrame:
    """Return DataFrame of categories with cashflow type and description."""
    categories = [
        ('ATM / Cash', 'expense', ''),
        ('Bars & Restaurants', 'expense', ''),
        ('Education', 'expense', ''),
        ('Finance & Insurances', 'expense', ''),
        ('Government', 'expense', ''),
        ('Entertainment', 'expense', ''),
        ('Mobility', 'expense', ''),
        ('Personal care', 'expense', ''),
        ('Services', 'expense', ''),
        ('Shopping', 'expense', ''),
        ('Utilities & Telecom', 'expense', ''),
        ('Housing', 'expense', ''),
        ('Other Expense', 'expense', ''),
        ('Salary', 'income', ''),
        ('Property', 'income', ''),
        ('Investment Income', 'income', ''),
        ('Other Income', 'income', ''),
        ('Savings', 'transfer', ''),
        ('Own Accounts', 'transfer', '')
    ]
    return pd.DataFrame(categories, columns=["name", "cashflow_type", "description"])


# ----------------------------
# Fiscal Years
# ----------------------------
def get_fiscal_years(engine) -> pd.DataFrame:
    """Generate fiscal years from 2020 until next year and filter out existing ones in DB."""
    start_year = 2020
    current_year = date.today().year
    end_year = current_year + 1

    fiscal_years = pd.DataFrame({'year': range(start_year, end_year)})
    fiscal_years['start_date'] = pd.to_datetime(fiscal_years['year'].astype(str) + '-01-01')
    fiscal_years['end_date'] = pd.to_datetime(fiscal_years['year'].astype(str) + '-12-31')

    # Filter out existing years from DB
    existing_years = pd.read_sql("SELECT year FROM fiscal_year", con=engine)
    fiscal_years = fiscal_years[~fiscal_years['year'].isin(existing_years['year'])]

    return fiscal_years

# ----------------------------
# Transactions
# ----------------------------
def get_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract relevant transaction columns and normalize names.
    """
    transactions = df[['account_number', 'counterparty_account_number', 'counterparty_name', 
                       'date', 'amount', 'balance']].copy()
    transactions.rename(columns={
        'account_number': 'account_id',
        'counterparty_account_number': 'counterparty_account_id',
    }, inplace=True)
    transactions['date'] = pd.to_datetime(transactions['date'], errors='coerce')
    return transactions