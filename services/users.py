from collections import defaultdict
from typing import MutableMapping

from sqlalchemy.ext.asyncio import AsyncSession

from common.settings import settings
from repositories.sqlalchemy.users.repositories import IUserRepository
from services.exceptions import BadDataException


async def validate_username(
    username: str,
    repository: IUserRepository,
    session: AsyncSession,
    errors: MutableMapping[str, list],
) -> list[str]:
    if len(username) < settings.minimal_username_length:
        errors['username'].append('Username is too short.')
    if await repository.check_exists(username, session):
        errors['username'].append('Username is already taken.')


async def create_user(
    repository: IUserRepository,
    session: AsyncSession,
    username: str,
):
    errors = defaultdict(list)
    await validate_username(username, repository, session, errors)

    if errors:
        raise BadDataException(errors)

    return await repository.create(username, session)
