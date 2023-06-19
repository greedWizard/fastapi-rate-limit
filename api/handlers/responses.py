from fastapi import Depends, HTTPException
from fastapi import Header
from fastapi.routing import APIRouter

from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies.responses import create_response_repository, verify_token
from api.dependencies.users import create_session
from api.schemas.responses import ResponseResponseSchema
from repositories.sqlalchemy.responses.repository import ResponseSQLAlchemyRepository


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
    session: AsyncSession = Depends(create_session),
    responses_repository: ResponseSQLAlchemyRepository = Depends(create_response_repository),
):
    return await responses_repository.fetch_data(session)
