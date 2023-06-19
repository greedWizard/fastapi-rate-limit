from datetime import datetime
from fastapi import Depends, HTTPException, Query, Request
from fastapi import Header
from fastapi.routing import APIRouter

from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies.api_keys import create_api_key_repository
from api.dependencies.responses import create_response_repository, verify_token
from api.dependencies.users import create_session
from api.schemas.responses import ResponseResponseSchema
from repositories.sqlalchemy.api_keys.repositories import IAPIKeyRepository
from repositories.sqlalchemy.responses.repository import ResponseSQLAlchemyRepository
from services.exceptions import LimitationException
from services.responses import create_response


router = APIRouter(prefix='/responses', tags=['responses'])


@router.get(
    '/',
    response_model=list[ResponseResponseSchema],
    operation_id='getResponses',
    description='Fetch list of responses',
    summary='Fetch list of responses',
    dependencies=[Depends(verify_token)]
)
async def fetch_responses_handler(
    request: Request,
    session: AsyncSession = Depends(create_session),
    api_key_repository: IAPIKeyRepository = Depends(create_api_key_repository),
    responses_repository: ResponseSQLAlchemyRepository = Depends(create_response_repository),
    limit: int = Query(default=10),
    offset: int = Query(default=0)
):
    response_code = status.HTTP_200_OK
    errors = None

    try:
        response_data = await responses_repository.fetch_data(
            str(request.url),
            session,
            limit,
            offset,
        )
    except LimitationException as exception:
        response_code = status.HTTP_429_TOO_MANY_REQUESTS
        errors = exception.errors

    await create_response(
        str(request.url),
        datetime.utcnow(),
        status_code=response_code,
        api_key_id=(await api_key_repository.get(key=request.headers['api-key'], session=session)).id,
        response_repository=responses_repository,
        session=session,
    )

    if errors:
        raise HTTPException(status_code=response_code, detail=errors)

    return response_data
