import logging

from models.Groups import GroupsModel
from models.Overview import OverviewModel
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException
from service.overview_abstract import OverviewAbstract
from sqlalchemy.sql import func


log = logging.getLogger("API_LOG")


class OverviewService(OverviewAbstract):
    def __init__(self, session=None):
        # Added session object for easier unittesting.
        self.session = session or Session

    def get_overview(self, userLender, userBorrower, groupID):
        try:
            with self.session(bind=engine, expire_on_commit=False) as session:
                query = session.query(OverviewModel)
                if userLender:
                    query = query.filter(OverviewModel.userIDLender == userLender)
                if userBorrower:
                    query = query.filter(OverviewModel.userIDBorrower == userBorrower)
                if groupID:
                    query = query.filter(OverviewModel.groupID == groupID)
                results = query.with_entities(func.sum(OverviewModel.amount).label('Sum_Amount')).all()
                results = {
                    "Lender": userLender,
                    "Borrower": userBorrower,
                    "Group": groupID,
                    "SumAmount": results[0].Sum_Amount
                }
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occurend : {err}",
            ) from err
        return {"record": results}
