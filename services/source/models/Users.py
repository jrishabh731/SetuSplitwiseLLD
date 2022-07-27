from config.db import Base
from sqlalchemy import Column, Integer, String, SMALLINT, Float, Date


class UsersModel(Base):
    __tablename__ = "users"
    userID = Column(String(30), primary_key=True, index=True)
    userName = Column(String(255))
