from config.db import Base
from sqlalchemy import Column, Integer, String, SMALLINT, Float, Date


class GroupsModel(Base):
    __tablename__ = "groups"
    groupID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    groupName = Column(String(255))
