import logging


log = logging.getLogger("API_LOG")


class ExpensesHandler:
    def __init__(self, ExpenseService):
        # Added ExpenseService object for easier unittesting.
        self.expense = ExpenseService()

    def get_expense(self, userID, startTime=None, endTime=None):
        return self.expense.get_expense(userID, startTime, endTime)

    def add_expense(self, expense):
        return self.expense.add_expense(expense)
