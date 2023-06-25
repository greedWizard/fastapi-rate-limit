from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    username: str
    date_joined: datetime = field(default_factory=datetime.utcnow)
    id: int | None = None

    def __eq__(self, __value: 'User') -> bool:
        return self.username == __value.username

    def __hash__(self) -> int:
        return hash(self.username)
