from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    username: str
    date_joined: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, __value: 'User') -> bool:
        return self.username == __value.username
