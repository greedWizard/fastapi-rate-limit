from datetime import datetime
from pydantic import BaseModel


class ResponseResponseSchema(BaseModel):
    responded_at: datetime
    status_code: int
    count: int
