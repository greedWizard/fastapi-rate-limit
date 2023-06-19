from typing import Protocol
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


class IUserRepository(Protocol):
    async def create(self, username: str, session: AsyncSession) -> User:
        ...

    async def check_exists_by_username(self, username: str, session: AsyncSession) -> bool:
        ...

    async def check_exists_by_id(self, id: int, session: AsyncSession) -> bool:
        ...

class SQLAlchemyUserRepository:
    async def create(self, username: str, session: AsyncSession) -> User:
        created_user = User(username=username)
        session.add(created_user)
        await session.commit()

        return created_user

    async def check_exists_by_username(self, username: str, session: AsyncSession) -> bool:
        return (await session.execute(
            select(func.count(User.id)
        ).where(User.username == username))).scalar() > 0

    async def check_exists_by_id(self, id: int, session: AsyncSession) -> bool:
        return (await session.execute(
            select(func.count(User.id)
        ).where(User.id == id))).scalar() > 0
