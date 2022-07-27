import logging
import datetime

from models.Expenses import ExpensesModel
from models.Transaction import TransactionModel
from models.GroupsMembership import GroupMembershipModel
from models.Groups import GroupsModel
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException
from sqlalchemy import Date, and_

log = logging.getLogger("API_LOG")


class SettlementHandler:
    def __init__(self, session=None):
        # Added session object for easier unittesting.
        self.session = session or Session