import logging


log = logging.getLogger("API_LOG")


class GroupsHandler:
    def __init__(self, GroupsService):
        self.group = GroupsService()

    def get_groups(self, groupID):
        return self.group.get_groups(groupID)

    def add_groups(self, group):
        return self.group.add_groups(group)
