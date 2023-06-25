from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy import func
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

    async def get_requests_count_from_time(
        self,
        api_key_id: str,
        last_time: datetime,
        session: AsyncSession,
    ) -> int:
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
    ) -> list[dict]:
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

    async def get_requests_count_from_time(
        self,
        api_key_id: int,
        last_time: datetime,
        session: AsyncSession,
    ) -> int:
        statement = select(func.count(Response.id)).where(
            Response.responded_at >= last_time,
            Response.responded_at <= datetime.utcnow(),
            Response.api_key_id == api_key_id,
        )
        
        return (await session.execute(statement)).scalar()
