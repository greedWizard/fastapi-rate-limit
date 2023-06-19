from datetime import datetime
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateResponseSchema(UserCreateSchema):
    id: int
    username: str
    date_joined: datetime

    class Config:
        orm_mode = True
