import abc


class UsersAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_users(self, users):
        pass

    @abc.abstractmethod
    def get_users(self, userID):
        pass
