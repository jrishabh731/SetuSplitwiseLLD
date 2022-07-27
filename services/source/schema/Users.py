from pydantic import BaseModel, validator, conint, constr


class Users(BaseModel):
    userID: str
    userName: str