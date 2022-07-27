import logging


log = logging.getLogger("API_LOG")


class UserHandler:
    def __init__(self, UserService):
        self.user = UserService()

    def get_users(self, userID):
        return self.user.get_users(userID)

    def add_users(self, users):
        return self.user.add_users(users)
