from collections import defaultdict
import pytest

from repositories.sqlalchemy.users.repositories import IUserRepository
from services.exceptions import BadDataException
from services.users import create_user, validate_username
from tests.factories import UserFactory
from tests.fixtures import FakeSession


@pytest.mark.asyncio
async def test_create_user_fail(
    user_repository: IUserRepository,
):
    session = FakeSession()
    user = UserFactory.create()
    session.add(user)

    with pytest.raises(BadDataException):
        await create_user(user_repository, session, user.username)


@pytest.mark.asyncio
async def test_create_user_success(
    user_repository: IUserRepository,
):
    session = FakeSession()
    await create_user(user_repository, session, 'username')

    assert len(session._objects)


@pytest.mark.asyncio
async def test_validate_user(
    user_repository: IUserRepository,
):
    session = FakeSession()
    errors = defaultdict(list)

    await validate_username('username', user_repository, session, errors)
    assert not errors

    user = UserFactory.create(username='12345679')
    session.add(user)

    await validate_username(user.username, user_repository, session, errors)
    assert len(errors['username']) == 1, errors

    await validate_username('u', user_repository, session, errors)
    assert len(errors['username']) == 3, errors
