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
        created_user = User(username=username)
        session.add(created_user)
        await session.commit()

        return created_user

    async def check_exists(self, username: str, session: AsyncSession) -> bool:
        return await session.execute(
            select(func.count(User.id)
        ).where(User.username == username)) > 0
