from datetime import datetime
from typing import Protocol

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from models.responses import Response
from repositories.sqlalchemy.responses.sql import FETCH_RESPONSES_DATA_SQL


class IResponseRepository(Protocol):
    async def create(
        self,
        api_key_id: int,
        status_code: int,
        responded_at: datetime,
        url: str,
        session: AsyncSession,
    ) -> Response:
        ...


class ResponseSQLAlchemyRepository:
    async def create(
        self,
        api_key_id: int,
        status_code: int,
        responded_at: datetime,
        url: str,
        session: AsyncSession,
    ) -> Response:
        new_response = Response(
            api_key_id=api_key_id,
            status_code=status_code,
            responded_at=responded_at,
            url=url,
        )
        session.add(new_response)
        await session.commit()

        return new_response

    async def fetch_data(
        self,
        url: str,
        session: AsyncSession,
        limit: int = 10,
        offset: int = 0,
    ) -> Response:
        results = await session.execute(text(FETCH_RESPONSES_DATA_SQL), params={
            'limit': limit,
            'offset': offset,
            'url': url,
        })
        return [{
            'responded_at': result[0],
            'status_code': result[1],
            'count': result[2],    
        } for result in results]
