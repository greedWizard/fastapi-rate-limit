from datetime import datetime
import pytest
from repositories.sqlalchemy.api_keys.repositories import IAPIKeyRepository

from repositories.sqlalchemy.users.repositories import IUserRepository
from tests.factories import APIKeyFactory, UserFactory
from tests.fixtures import FakeSession


@pytest.mark.asyncio
async def test_user_repository_create(
    user_repository: IUserRepository,
):
    session = FakeSession()
    await user_repository.create('username', session)
    
    assert len(session._objects)


@pytest.mark.asyncio
async def test_user_repository_exists(
    user_repository: IUserRepository,
):
    session = FakeSession()
    user = UserFactory.create()
    session.add(user)

    exists = await user_repository.check_exists_by_username(username=user.username, session=session)
    assert exists
    
    exists = await user_repository.check_exists_by_username(username='nonexistingusername', session=session)
    assert not exists


@pytest.mark.asyncio
async def test_api_key_repository_create(
    api_key_repository: IAPIKeyRepository,
):
    session = FakeSession()
    await api_key_repository.create(123, session)
    
    assert len(session._objects)


@pytest.mark.asyncio
async def test_api_key_repository_update(
    api_key_repository: IAPIKeyRepository,
):
    session = FakeSession()
    key = '12345'
    api_key = APIKeyFactory.create(key=key)
    session.add(api_key)
    last_used = datetime.utcnow()

    await api_key_repository.update(key=key, session=session, last_used=last_used, banned_at=datetime.utcnow())
    
    assert api_key.banned_at
    assert api_key.last_used == last_used
