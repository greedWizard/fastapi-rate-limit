from dataclasses import dataclass, field
from datetime import datetime

from models.users import User


@dataclass
class APIKey:
    key: str
    user_id: int
    id: int| None = None
    user: User | None = None
    last_used: datetime | None = None
    is_banned: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, __value: 'APIKey') -> bool:
        return self.key == __value.key

    def __hash__(self) -> int:
        return hash(self.key)
