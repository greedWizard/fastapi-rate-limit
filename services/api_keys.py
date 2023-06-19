from collections import defaultdict
from typing import MutableMapping

from sqlalchemy.ext.asyncio import AsyncSession

from models.api_keys import APIKey
from repositories.sqlalchemy.api_keys.repositories import IAPIKeyRepository
from repositories.sqlalchemy.users.repositories import IUserRepository
from services.exceptions import BadDataException


async def validate_user_id(
    user_id: int,
    user_repository: IUserRepository,
    session: AsyncSession,
    errors: MutableMapping[str, list],
):
    if not await user_repository.check_exists_by_id(user_id, session):
        errors['user_id'].append('User does not exist!')


async def create_api_key(
    user_id: int,
    user_repository: IUserRepository,
    api_key_repository: IAPIKeyRepository,
    session: AsyncSession,
) -> APIKey:
    errors = defaultdict(list)
    await validate_user_id(user_id, user_repository, session, errors)

    if errors:
        raise BadDataException(errors)

    return await api_key_repository.create(user_id, session)
