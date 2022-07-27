from pydantic import BaseModel
from typing import List


class Groups(BaseModel):
    groupName: str
    groupMembers: List[str]