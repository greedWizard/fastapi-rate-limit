from dataclasses import dataclass, field
from datetime import datetime
from models.api_keys import APIKey


@dataclass
class Response:
    id: int
    api_key_id: int
    status_code: int
    api_key: APIKey | None = None
    responded_at: datetime = field(default_factory=datetime.utcnow)

    def __eq__(self, __value: 'Response') -> bool:
        return (
            self.key == __value.status_code
            and self.status_code == __value.status_code
            and self.responded_at == __value.responded_at
            and self.api_key_id == __value.api_key_id
        )

    def __hash__(self) -> int:
        return hash(
            ''.join((
                str(self.api_key_id),
                str(self.status_code),
                str(self.responded_at),
                str(self.api_key_id),
            ))
        )
