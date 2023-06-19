from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.users import create_session, create_user_repository
from api.schemas.users import UserCreateResponseSchema, UserCreateSchema
from repositories.sqlalchemy.users.repositories import IUserRepository
from services.exceptions import BadDataException
from services.users import create_user


router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserCreateResponseSchema,
    operation_id='createUser',
    description='Create new user with API key',
    summary='Create new user',
)
async def create_user_handler(
    user_create_schema: UserCreateSchema,
    session: AsyncSession = Depends(create_session),
    user_repository: IUserRepository = Depends(create_user_repository)
):
    try:
        user = await create_user(
            user_repository,
            session,
            user_create_schema.username,
        )
    except BadDataException as exception:
        await session.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.errors)

    await session.close()
    return user
