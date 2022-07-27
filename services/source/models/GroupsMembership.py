from config.db import Base
from sqlalchemy import Column, Integer, String, SMALLINT, Float, Date, ForeignKey


class GroupMembershipModel(Base):
    __tablename__ = "groups_membership"
    groupID = Column(Integer, ForeignKey("groups.groupID"), primary_key=True)
    userID = Column(String(30), ForeignKey("users.userID"), primary_key=True)

