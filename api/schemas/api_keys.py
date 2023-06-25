from datetime import datetime
from pydantic import BaseModel

from models.users import User


class APIKeyResponseSchema(BaseModel):
    key: str
    last_used: datetime | None
    banned_at: datetime | None
    created_at: datetime

    class Config:
        orm_mode = True