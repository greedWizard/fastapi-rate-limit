from dataclasses import dataclass, field
import random

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
