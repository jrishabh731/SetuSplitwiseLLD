from config.db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey


class ExpensesModel(Base):
    __tablename__ = "expenses"
    expenseID = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(String(30), ForeignKey("users.userID"))
    groupID = Column(Integer, ForeignKey("groups.groupID"))
    amountPaid = Column(Float)
    splitType = Column(String(255))
    expenseTimestamp = Column(DateTime)