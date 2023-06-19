from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from fastapi import Depends, Header, HTTPException, Request

from api.dependencies.api_keys import create_api_key_repository
from api.dependencies.users import create_session
from repositories.sqlalchemy.api_keys.repositories import IAPIKeyRepository
from repositories.sqlalchemy.responses.repository import IResponseRepository, ResponseSQLAlchemyRepository
from services.api_keys import verify_api_key_rate_limit, verify_api_key_token
from services.exceptions import LimitationException, SecurityException, UserBannedException
from services.responses import create_response


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


async def verify_rate_limit(
    request: Request,
    api_key: Annotated[str, Header()],
    api_key_repository: IAPIKeyRepository = Depends(create_api_key_repository),
    response_repository: IResponseRepository = Depends(create_response_repository),
    session: AsyncSession = Depends(create_session),
):
    errors = None

    try:
        await verify_api_key_rate_limit(api_key, api_key_repository, response_repository, session)
        status_code = status.HTTP_200_OK
    except LimitationException as exception:
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
        errors = exception.errors
    except UserBannedException as exception:
        status_code = status.HTTP_418_IM_A_TEAPOT
        errors = exception.errors

    await create_response(
        str(request.url),
        datetime.utcnow(),
        status_code=status_code,
        api_key_id=(await api_key_repository.get(key=api_key, session=session)).id,
        response_repository=response_repository,
        session=session,
    )

    if errors:
        raise HTTPException(status_code=status_code, detail=errors)
