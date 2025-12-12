from sqlalchemy import Column, Integer, Date, UniqueConstraint

def FiscalYear(Base):
    class FiscalYear(Base):
        __tablename__ = "fiscal_year"

        fiscal_year_id = Column(Integer, primary_key=True)
        year = Column(Integer, nullable=False, unique=True)
        start_date = Column(Date, nullable=False)
        end_date = Column(Date, nullable=False)

        __table_args__ = (UniqueConstraint("year", name="uq_year"),)
    return FiscalYear
