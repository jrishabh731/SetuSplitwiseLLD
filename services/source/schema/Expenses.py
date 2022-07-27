from pydantic import BaseModel
from typing import Dict


class Expenses(BaseModel):
    userID: str
    groupID: str
    amountPaid: float
    splitType: str
    splitMap: Dict