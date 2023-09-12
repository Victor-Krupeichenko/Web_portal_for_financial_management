from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from flask_login import UserMixin
Base = declarative_base()


class User(Base, UserMixin):
    """
    Модель таблицы базы данных users
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    account = relationship("Account", cascade="all, delete", backref="accaunt")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"{self.username}"


class Account(Base):
    """
    Модель таблицы базы данных accounts
    """

    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    balance = Column(Float(), default=0.0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete")

    def __repr__(self):
        return f"{self.name}"


class Transaction(Base):
    """
    Модель таблицы базы данных transactions
    """

    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    transaction_type = Column(String(), nullable=False)
    amount = Column(Float(), nullable=False)
    date = Column(DateTime(), default=datetime.utcnow())
    description = Column(String(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"{self.transaction_type}"
