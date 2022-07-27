import logging


log = logging.getLogger("API_LOG")


class OverviewHandler:
    def __init__(self, OverviewService):
        self.overview = OverviewService()

    def get_overview(self, userLender, userBorrower, groupID):
        return self.overview.get_overview(userLender, userBorrower, groupID)