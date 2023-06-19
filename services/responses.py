from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy.responses.repository import IResponseRepository


async def create_response(
    url: str,
    responded_at: datetime,
    status_code: int,
    api_key_id: int, 
    response_repository: IResponseRepository,
    session: AsyncSession,
):
    # TODO: verify status_code
    return await response_repository.create(
        api_key_id,
        status_code,
        responded_at,
        url,
        session,
    )