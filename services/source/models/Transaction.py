from config.db import Base
from sqlalchemy import Column, Integer, String, SMALLINT, Float, DateTime, ForeignKey, Boolean


class TransactionModel(Base):
    __tablename__ = "transaction"
    transactionID = Column(Integer, primary_key=True, autoincrement=True)
    transactionTimestamp = Column(DateTime, index=True)
    expenseID = Column(Integer, ForeignKey("expenses.expenseID"))
    groupID = Column(Integer, ForeignKey("groups.groupID"))
    userBorrower = Column(String(30), ForeignKey("users.userID"))
    userLender = Column(String(30), ForeignKey("users.userID"))
    amountPaid = Column(Float)
    settlementTimestamp = Column(DateTime, default=None)
    SettlementStatus = Column(Boolean, default=False)
