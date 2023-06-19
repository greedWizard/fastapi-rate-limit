from asyncio import Protocol
from typing import Iterable
import uuid
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from models.api_keys import APIKey


class IAPIKeyRepository(Protocol):
    async def create(self, user_id: int, session: AsyncSession) -> APIKey:
        ...

    async def update(
        self,
        key: str,
        session: AsyncSession,
        **update_values,
    ) -> APIKey:
        ...

    async def fetch(self, session: AsyncSession, limit: int = 10, offset: int = 0, ) -> Iterable[APIKey]:
        ...


class APIKeySQLAlchemyRepository(Protocol):
    async def create(self, user_id: int, session: AsyncSession) -> APIKey:
        created_key = APIKey(key=str(uuid.uuid4()), user_id=user_id)
        session.add(created_key)

        await session.commit()
        return created_key

    async def update(
        self,
        key: str,
        session: AsyncSession,
        **update_values,
    ):
        statement = update(APIKey).where(APIKey.key == key).values(**update_values)
        
        await session.execute(statement)
        await session.commit()
