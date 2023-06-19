from datetime import datetime
from pydantic import BaseModel

from api.schemas.api_keys import APIKeyResponseSchema


class UserCreateSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateResponseSchema(UserCreateSchema):
    id: int
    username: str
    date_joined: datetime
    api_key: APIKeyResponseSchema

    class Config:
        orm_mode = True
