from collections import defaultdict
from datetime import datetime
from typing import MutableMapping

from sqlalchemy.ext.asyncio import AsyncSession

from common.settings import settings
from models.api_keys import APIKey
from repositories.sqlalchemy.api_keys.repositories import IAPIKeyRepository
from repositories.sqlalchemy.responses.repository import IResponseRepository
from repositories.sqlalchemy.users.repositories import IUserRepository
from services.exceptions import BadDataException, LimitationException, SecurityException, UserBannedException


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


async def verify_api_key_token(
    api_key: str,
    api_key_repository: IAPIKeyRepository,
    session: AsyncSession,
):
    api_key_object = await api_key_repository.get(key=api_key, session=session)

    if not api_key_object:
        raise SecurityException({'api_key': ['API key does not exist']})


async def check_api_key_limitations(
    api_key_id: int,
    api_key: str,
    banned_at: datetime,
    api_key_repository: IAPIKeyRepository,
    response_repository: IResponseRepository,
    session: AsyncSession,
):
    requests_count = await response_repository.get_requests_count_from_time(
        api_key_id,
        datetime.utcnow() - settings.limitations_delta,
        session,
    )

    if requests_count <= settings.limitations_count and requests_count > 1:
        raise LimitationException(errors={'api_key': ['Too many requests.']})
    elif requests_count > settings.limitations_count:
        await api_key_repository.update(api_key, session, banned_at=datetime.utcnow())
        raise UserBannedException(errors={'api_key': ['Your API key is banned :(']})
    elif (
        requests_count == 0
        and banned_at
        and (datetime.utcnow() - banned_at).seconds >= settings.ban_duration.seconds
    ):
        await api_key_repository.update(api_key, session, banned_at=None)


async def verify_api_key_rate_limit(
    api_key: str,
    api_key_repository: IAPIKeyRepository,
    response_repository: IResponseRepository,
    session: AsyncSession,
):
    api_key_object = await api_key_repository.get(api_key, session)

    await check_api_key_limitations(
        api_key_object.id,
        api_key_object.key,
        api_key_object.banned_at,
        api_key_repository,
        response_repository,
        session,
    )
