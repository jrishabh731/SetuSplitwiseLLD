from config.db import Base
from sqlalchemy import Column, Integer, String, SMALLINT, Float, Date, ForeignKey


class OverviewModel(Base):
    __tablename__ = "overview"
    userIDLender = Column(String(30), ForeignKey("users.userID"), primary_key=True)
    userIDBorrower = Column(String(30), ForeignKey("users.userID"), primary_key=True)
    groupID = Column(Integer, ForeignKey("groups.groupID"), primary_key=True)
    amount = Column(Float)