import abc


class ExpensesAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_expense(self, userID, startTime=None, endTime=None):
        pass

    @abc.abstractmethod
    def add_expense(self, expense):
        pass