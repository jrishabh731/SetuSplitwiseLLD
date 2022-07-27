import logging
import datetime

from models.Expenses import ExpensesModel
from models.Transaction import TransactionModel
from models.Overview import OverviewModel
from models.GroupsMembership import GroupMembershipModel
from models.Groups import GroupsModel
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException
from sqlalchemy import Date, and_
from service.expenses_abstract import ExpensesAbstract

log = logging.getLogger("API_LOG")


class ExpensesService(ExpensesAbstract):
    def __init__(self, session=None):
        # Added session object for easier unittesting.
        self.session = session or Session

    def get_expense(self, userID, startTime=None, endTime=None):
        try:
            lend = 0
            borrow = 0
            self_ = 0
            all_transactions = []
            detailed_result = {
                "transactions": all_transactions,
                "detail": {
                    "borrowed": 0,
                    "lent": 0,
                    "self": 0
                }
            }
            with self.session(bind=engine, expire_on_commit=False) as session:
                query = session.query(TransactionModel, ExpensesModel, GroupsModel). \
                    join(ExpensesModel, TransactionModel.expenseID == ExpensesModel.expenseID). \
                    join(GroupsModel, TransactionModel.groupID == GroupsModel.groupID)

                if startTime:
                    query = query.filter(TransactionModel.transactionTimestamp.cast(Date) >= startTime)

                if endTime:
                    query = query.filter(TransactionModel.transactionTimestamp.cast(Date) <= endTime)

                lend_query = query.filter(and_(TransactionModel.userBorrower != userID,
                                               TransactionModel.userLender == userID)).all()
                borrow_query = query.filter(and_(TransactionModel.userBorrower == userID,
                                                 TransactionModel.userLender != userID)).all()
                self_transactions = query.filter(and_(TransactionModel.userBorrower == userID,
                                                      TransactionModel.userLender == userID)).all()

                for transaction, expense, groups in lend_query:
                    transactions = {
                        "transactionTimestamp": transaction.transactionTimestamp,
                        "amountPaid": transaction.amountPaid,
                        "expenseAmount": expense.amountPaid,
                        "group": groups.groupName,
                    }
                    all_transactions.append(transactions)
                    lend += transaction.amountPaid

                for transaction, expense, groups in borrow_query:
                    transactions = {
                        "transactionTimestamp": transaction.transactionTimestamp,
                        "amountPaid": -1 * transaction.amountPaid,
                        "expenseAmount": expense.amountPaid,
                        "group": groups.groupName,
                    }
                    all_transactions.append(transactions)
                    borrow += -1 * transaction.amountPaid

                for transaction, expense, groups in self_transactions:
                    transactions = {
                        "transactionTimestamp": transaction.transactionTimestamp,
                        "amountPaid": -1 * transaction.amountPaid,
                        "expenseAmount": expense.amountPaid,
                        "group": groups.groupName,
                    }
                    all_transactions.append(transactions)
                    self_ += -1 * transaction.amountPaid

            detailed_result["detail"] = {
                "borrowed": borrow,
                "lend": lend,
                "self": self_
            }
        except Exception as err:
            log.error(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err
        return detailed_result

    def add_expense(self, expense):
        try:
            import pdb
            pdb.set_trace()
            with self.session(bind=engine, expire_on_commit=False) as session:
                split_map = expense.splitMap
                del expense.splitMap
                expenseObj = ExpensesModel(**expense.dict())
                expenseObj.expenseTimestamp = datetime.datetime.now()
                session.add(expenseObj)
                session.flush()

                users_current_group = session.query(GroupMembershipModel). \
                    filter(GroupMembershipModel.groupID == expenseObj.groupID). \
                    with_entities(GroupMembershipModel.userID).all()

                for user in users_current_group:
                    if expenseObj.splitType == "equal":
                        curr_amount = (expenseObj.amountPaid / len(users_current_group))
                    else:
                        curr_amount = split_map[user[0]]

                    transactionalData = TransactionModel(
                        transactionTimestamp=datetime.datetime.now(),
                        expenseID=expenseObj.expenseID,
                        groupID=expenseObj.groupID,
                        userLender=expenseObj.userID,
                        userBorrower=user[0],
                        amountPaid=curr_amount
                    )
                    session.add(transactionalData)

                    result = session.query(OverviewModel).filter(
                        OverviewModel.userIDLender == expenseObj.userID,
                        OverviewModel.userIDBorrower == user[0],
                        OverviewModel.groupID == expenseObj.groupID).first()

                    if result is None:
                        overview_map = OverviewModel(
                            userIDLender=expenseObj.userID,
                            userIDBorrower=user[0],
                            groupID=expenseObj.groupID,
                            amount=curr_amount
                        )
                        session.add(overview_map)
                    else:
                        result.amount += curr_amount

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
