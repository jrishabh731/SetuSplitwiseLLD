import abc


class GroupsAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_groups(self, users):
        pass

    @abc.abstractmethod
    def get_groups(self, userID):
        pass
