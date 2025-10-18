import pandas as pd
from sqlalchemy import create_engine

from ..utils.helper_functions import is_new

def get_engine():
    """Create and return a PostgreSQL engine."""
    return create_engine("postgresql://arthur:arthur@localhost:5432/finances_db")

# ----------------------------
# Insert Functions
# ----------------------------
def save_fiscal_years(fiscal_years: pd.DataFrame, engine) -> None:
    fiscal_years.to_sql(
        name='fiscal_year',
        con=engine,
        if_exists='append',
        index=False
    )
    print("Fiscal years inserted successfully.")


def save_categories(categories: pd.DataFrame, engine) -> None:
    categories.to_sql(
        name='category',
        con=engine,
        if_exists='append',
        index=False
    )
    print("Categories inserted successfully.")


def save_internal_accounts(internal_accounts: pd.DataFrame, engine) -> None:
    existing_accounts = pd.read_sql("SELECT * FROM account", con=engine)

    accounts_to_add = internal_accounts[
        internal_accounts.apply(is_new, axis=1, existing=existing_accounts)
    ]

    if not accounts_to_add.empty:
        accounts_to_add.to_sql(
            name='account',
            con=engine,
            if_exists='append',
            index=False
        )
    
    print("Internal accounts inserted successfully.")


def save_new_accounts(accounts: pd.DataFrame, engine, internal_accounts: pd.DataFrame) -> None:
    """
    Save only new external accounts to the database.
    Internal accounts are excluded automatically.
    """
    # keep only external accounts
    accounts = accounts[accounts['type'] == 'external']

    # Load existing accounts from DB
    existing_accounts = pd.read_sql("SELECT * FROM account", con=engine)

    # Filter truly new accounts
    accounts_to_add = accounts[accounts.apply(is_new, axis=1, existing=existing_accounts)]

    # Insert remaining accounts
    if not accounts_to_add.empty:
        accounts_to_add.to_sql(
            name='account',
            con=engine,
            if_exists='append',
            index=False
        )

    print("Accounts inserted successfully.")

def map_fiscal_year(transactions: pd.DataFrame, engine) -> pd.DataFrame:
    """Add fiscal_year foreign key to transactions based on the date."""
    fiscal_years = pd.read_sql("SELECT * FROM fiscal_year", con=engine)
    fiscal_years['start_date'] = pd.to_datetime(fiscal_years['start_date'])
    fiscal_years['end_date'] = pd.to_datetime(fiscal_years['end_date'])

    def get_fiscal_id(date):
        fy = fiscal_years[(fiscal_years['start_date'] <= date) & (fiscal_years['end_date'] >= date)]
        return fy['fiscal_year_id'].iloc[0] if not fy.empty else None

    transactions['fiscal_id'] = transactions['date'].apply(get_fiscal_id)
    return transactions


def map_accounts(transactions: pd.DataFrame, engine) -> pd.DataFrame:
    """
    Map account_id and counterparty_account_id to DB IDs using a mapping dictionary.
    """
    accounts = pd.read_sql("SELECT * FROM account", con=engine)
    
    # Create a mapping dictionary: account_key -> account_id
    accounts['account_key'] = accounts['iban'].fillna(accounts['name'])
    account_map = accounts.set_index('account_key')['account_id'].to_dict()

    # Map main account (assume transactions['account_id'] contains IBAN)
    transactions['account_id'] = transactions['account_id'].map(account_map)

    # Map counterparty account
    def map_counterparty(row):
        key = row['counterparty_account_id'] if pd.notna(row['counterparty_account_id']) else row['counterparty_name']
        return account_map.get(key)  # returns account_id or None if not found

    transactions['counterparty_account_id'] = transactions.apply(map_counterparty, axis=1)

    return transactions


def save_transactions(transactions: pd.DataFrame, engine) -> None:
    """Insert transactions into the database."""
    transactions = transactions[[
            'account_id',
            'counterparty_account_id',
            'date',
            'amount',
            'balance',
            'fiscal_id'
        ]]

    if not transactions.empty:
        transactions.to_sql(
            'transaction',
            con=engine,
            if_exists='append',
            index=False
        )
        print("Transactions inserted successfully.")