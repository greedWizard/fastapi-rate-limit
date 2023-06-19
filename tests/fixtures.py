from dataclasses import dataclass, field
import random
import uuid
from models.api_keys import APIKey

from models.users import User


@dataclass
class FakeSession:
    _is_closed: bool = False
    _is_commited: bool = False
    _objects: list = field(default_factory=list)

    async def commit(self, *args, **kwargs):
        self._is_commited = True

        for obj in self._objects:
            obj.id = random.randint(1, 100)


    async def close(self, *args, **kwargs):
        self._is_closed = True

    def add(self, object: object, *args, **kwargs):
        self._objects.append(object)
        

class FakeUserRepository:
    async def create(self, username: str, session: FakeSession) -> User:
        created_user = User(username=username)
        session.add(created_user)
        await session.commit()

        return created_user

    async def check_exists(self, username: str, session: FakeSession) -> bool:
        return len(
            [user for user in session._objects if user.username == username]
        ) > 0


class FakeAPIKeyRepository:
    async def create(self, user_id: int, session: FakeSession) -> APIKey:
        created_key = APIKey(key=uuid.uuid4(), user_id=user_id)
        session.add(created_key)

        await session.commit()
        return created_key

    async def update(
        self,
        key: str,
        session: FakeSession,
        **update_values,
    ):
        updated_object = next(
            obj for obj in session._objects if obj.key == key
        )

        for field, value in update_values.items():
            setattr(updated_object, field, value)

        session.add(updated_object)
        await session.commit()

        return updated_object
