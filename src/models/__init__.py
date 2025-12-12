from .base import get_base
from .category import Category as CategoryFactory
from .fiscal_year import FiscalYear as FiscalYearFactory
from .account import Account as AccountFactory
from .transaction import Transaction as TransactionFactory

def load_models(schema: str):
    """Dynamically create models bound to a given schema."""
    Base = get_base(schema)

    Category = CategoryFactory(Base)
    FiscalYear = FiscalYearFactory(Base)
    Account = AccountFactory(Base, Category)
    Transaction = TransactionFactory(Base, Account, FiscalYear)

    return {
        "Base": Base,
        "Category": Category,
        "FiscalYear": FiscalYear,
        "Account": Account,
        "Transaction": Transaction,
    }
