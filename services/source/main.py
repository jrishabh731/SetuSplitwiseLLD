"""
This file will hold the endpoints and there respective handlers.
"""
import sys
print(sys.path)
import logger
import logging
from datetime import datetime

from fastapi import FastAPI, status
from typing import Union

from config.db import Base, engine

from handlers.Groups import GroupsHandler
from handlers.Users import UserHandler
from handlers.Expenses import ExpensesHandler
from handlers.Overview import OverviewHandler
from schema.Groups import Groups
from schema.Users import Users
from schema.Expenses import Expenses
from service.groups_service import GroupsService
from service.users_service import UsersService
from service.expenses_service import ExpensesService
from service.overview_service import OverviewService


Base.metadata.create_all(engine)

log = logging.getLogger("API_LOG")
app = FastAPI()


@app.get("/groups", status_code=status.HTTP_200_OK)
def get_users(groupID: str):
    log.info(f"Received get requests for Appointment ID : {groupID}")
    return GroupsHandler(GroupsService).get_groups(groupID)


@app.post("/groups", status_code=status.HTTP_200_OK)
def add_group(groups: Groups):
    return GroupsHandler(GroupsService).add_groups(groups)


@app.get("/users", status_code=status.HTTP_200_OK)
def get_users(userID: str):
    log.info(f"Received get requests for Appointment ID : {userID}")
    return UserHandler(UsersService).get_users(userID)


@app.post("/users/", status_code=status.HTTP_200_OK)
def create_user(user: Users):
    return UserHandler(UsersService).add_users(user)


@app.get("/expenses", status_code=status.HTTP_200_OK)
def get_expenses(userID: str, startTime: Union[str, None] = None, endTime: Union[str, None] = None):
    if startTime:
        startTime = datetime.strptime(startTime, "%Y-%m-%d").date()
    if endTime:
        endTime = datetime.strptime(endTime, "%Y-%m-%d").date()
    return ExpensesHandler(ExpensesService).get_expense(userID, startTime, endTime)


@app.post("/expenses", status_code=status.HTTP_200_OK)
def add_expense(expense: Expenses):
    return ExpensesHandler(ExpensesService).add_expense(expense)


@app.get("/overview", status_code=status.HTTP_200_OK)
def get_overview(userLender: Union[str, None] = None, userBorrower: Union[str, None] = None,
                 groupID: Union[str, None] = None):
    return OverviewHandler(OverviewService).get_overview(userLender, userBorrower, groupID)
