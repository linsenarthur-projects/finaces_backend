from sqlalchemy import Column, Integer, String, Text, CheckConstraint

def Category(Base):
    class Category(Base):
        __tablename__ = "category"

        category_id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        cashflow_type = Column(String(20), nullable=False)
        description = Column(Text)

        __table_args__ = (
            CheckConstraint("cashflow_type IN ('income', 'expense', 'transfer')", name="check_cashflow_type"),
        )
    return Category
