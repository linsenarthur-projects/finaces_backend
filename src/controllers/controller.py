from utils.file_reader import upload_csv
from utils.file_transformer import clean_and_transform_data
from utils.data_generator import (
    get_internal_accounts, 
    get_accounts_from_data, 
    get_categories, 
    get_fiscal_years,
    get_transactions
)
from repository.repository import (
    get_engine, 
    save_fiscal_years, 
    save_categories,
    save_internal_accounts, 
    save_new_accounts,
    map_fiscal_year,
    map_accounts,
    save_transactions
)

def process_csv(file: str):
    """
    Process and clean the CSV file.
    Returns the cleaned DataFrame.
    """
    df = upload_csv(file)
    df = clean_and_transform_data(df)
    return df

def prepare_dataframes(df):
    """
    Prepare all DataFrames for DB insertion and create DB engine.
    Returns a tuple: (engine, internal_accounts, accounts, categories, fiscal_years)
    """
    engine = get_engine()
    internal_accounts = get_internal_accounts()
    accounts = get_accounts_from_data(df, internal_accounts)
    categories = get_categories()
    fiscal_years = get_fiscal_years(engine)
    transactions = get_transactions(df)
    return engine, internal_accounts, accounts, categories, fiscal_years, transactions

def save_to_db(engine, internal_accounts, accounts, categories, fiscal_years, transactions):
    """Save all prepared DataFrames to the database."""
    save_fiscal_years(fiscal_years, engine)
    save_categories(categories, engine)
    save_internal_accounts(internal_accounts, engine)
    save_new_accounts(accounts, engine, internal_accounts)
    transactions = map_fiscal_year(transactions, engine)
    transactions = map_accounts(transactions, engine)
    save_transactions(transactions, engine)

def process_csv_and_save_to_db(file: str):
    df = process_csv(file)
    engine, internal_accounts, accounts, categories, fiscal_years, transactions = prepare_dataframes(df)
    save_to_db(engine, internal_accounts, accounts, categories, fiscal_years, transactions)
    return df