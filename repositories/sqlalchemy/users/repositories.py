from typing import Protocol
from sqlalchemy import func, select

from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


class IUserRepository(Protocol):
    async def create(self, username: str, session: AsyncSession) -> User:
        ...

    async def check_exists(self, username: str, session: AsyncSession) -> bool:
        ...


class SQLAlchemyUserRepository:
    async def create(self, username: str, session: AsyncSession) -> User:
        session.add(User(username=username))
        await session.commit()

    async def check_exists(self, username: str, session: AsyncSession) -> bool:
        return await session.execute(
            select(func.count(User.id)
        ).where(User.username == username)) > 0
