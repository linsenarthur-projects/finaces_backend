from sqlalchemy import Column, Integer, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship

def Transaction(Base, Account, FiscalYear):
    class Transaction(Base):
        __tablename__ = "transaction"

        transaction_id = Column(Integer, primary_key=True)
        account_id = Column(Integer, ForeignKey(f"{Base.metadata.schema}.account.account_id"), nullable=False)
        counterparty_account_id = Column(Integer, ForeignKey(f"{Base.metadata.schema}.account.account_id"))
        date = Column(Date, nullable=False)
        amount = Column(Numeric(12, 2), nullable=False)
        balance = Column(Numeric(12, 2), nullable=False)
        fiscal_id = Column(Integer, ForeignKey(f"{Base.metadata.schema}.fiscal_year.fiscal_year_id"), nullable=False)
        description = Column(Text)

        account = relationship(Account, foreign_keys=[account_id])
        counterparty_account = relationship(Account, foreign_keys=[counterparty_account_id])
        fiscal_year = relationship(FiscalYear)
    return Transaction
