import abc


class OverviewAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_overview(self, userLender, userBorrower, groupID):
        pass
