from dataclasses import dataclass
from datetime import datetime


@dataclass
class APIKey:
    key: str
    last_used: datetime = None
    is_banned: bool = False

    def __eq__(self, __value: 'APIKey') -> bool:
        return self.key == __value.key
