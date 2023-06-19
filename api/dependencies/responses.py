from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from fastapi import Depends, Header, HTTPException

from api.dependencies.api_keys import create_api_key_repository
from api.dependencies.users import create_session
from repositories.sqlalchemy.responses.repository import ResponseSQLAlchemyRepository
from services.api_keys import verify_api_key_token
from services.exceptions import SecurityException


def create_response_repository():
    return ResponseSQLAlchemyRepository()


async def verify_token(
    api_key: Annotated[str, Header()],
    api_key_repository = Depends(create_api_key_repository),
    session: AsyncSession = Depends(create_session),
):
    try:
        await verify_api_key_token(api_key, api_key_repository, session)
    except SecurityException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.errors)
