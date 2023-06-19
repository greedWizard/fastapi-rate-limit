from datetime import datetime
from pydantic import BaseModel


class ResponseResponseSchema(BaseModel):
    responded_at: datetime
    response_status: int
