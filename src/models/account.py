from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

def Account(Base, Category):
    class Account(Base):
        __tablename__ = "account"

        account_id = Column(Integer, primary_key=True)
        iban = Column(String(100))
        name = Column(String(250), nullable=False)
        nickname = Column(String(250))
        category_id = Column(Integer, ForeignKey(f"{Base.metadata.schema}.category.category_id"), default=1)
        type = Column(String(20), nullable=False, default="external")
        description = Column(Text)

        category = relationship(Category)

        __table_args__ = (
            CheckConstraint("type IN ('internal', 'external')", name="check_account_type"),
        )
    return Account
