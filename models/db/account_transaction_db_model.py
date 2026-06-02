from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class AccountTransactionTemplate(Base):
    __tablename__ = "accounts_transaction_template"
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)
