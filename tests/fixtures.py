from dataclasses import dataclass, field

from models.users import User


@dataclass
class FakeSession:
    _objects: list = field(default_factory=list)

    async def commit(self, *args, **kwargs):
        ...

    def add(self, object: object, *args, **kwargs):
        self._objects.append(object)
        

class FakeUserRepository:
    async def create(self, username: str, session: FakeSession) -> User:
        session.add(User(username=username))
        await session.commit()

    async def check_exists(self, username: str, session: FakeSession) -> bool:
        return len(
            [user for user in session._objects if user.username == username]
        ) > 0
