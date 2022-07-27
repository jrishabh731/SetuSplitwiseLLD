import logging

from models.Groups import GroupsModel
from models.GroupsMembership import GroupMembershipModel
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException
from service.groups_abstract import GroupsAbstract


log = logging.getLogger("API_LOG")


class GroupsService(GroupsAbstract):
    def __init__(self, session=None):
        # Added session object for easier unittesting.
        self.session = session or Session

    def get_groups(self, userID):
        record = []
        try:
            with self.session(bind=engine, expire_on_commit=False) as session:
                record = session.query(GroupsModel).get(userID)
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err
        return {"record": record}

    def add_groups(self, group):
        try:
            result = {}
            with self.session(bind=engine, expire_on_commit=False) as session:
                group_members = group.groupMembers
                del group.groupMembers
                group_obj = GroupsModel(**group.dict())
                session.add(group_obj)
                session.flush()
                for member in group_members:
                    session.add(GroupMembershipModel(**{"groupID": group_obj.groupID, "userID": member}))
                try:
                    session.commit()
                    result["groupID"] = [group_obj.groupID]
                except Exception as err:
                    log.error(f"Exception occured: {err}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Exception occured : {err}",
                    ) from err
            return result
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err

