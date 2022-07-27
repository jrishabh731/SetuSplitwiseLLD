import logging

from models.Users import UsersModel
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException
from service.users_abstract import UsersAbstract

log = logging.getLogger("API_LOG")


class UsersService(UsersAbstract):
    def __init__(self, session=None):
        # Added session object for easier unittesting.
        self.session = session or Session

    def get_users(self, userID):
        record = []
        try:
            with self.session(bind=engine, expire_on_commit=False) as session:
                record = session.query(UsersModel).get(userID)
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err
        return {"record": record}

    def add_users(self, users):
        try:
            with self.session(bind=engine, expire_on_commit=False) as session:
                session.add(UsersModel(**users.dict()))
                try:
                    session.commit()
                    return {"status": True}
                except Exception as err:
                    log.error(f"Exception occured: {err}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Exception occured : {err}",
                    ) from err
            return {"status": False}
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err

