import pytest

from repositories.sqlalchemy.users.repositories import IUserRepository
from tests.factories import UserFactory
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

    exists = await user_repository.check_exists(username=user.username, session=session)
    assert exists
    
    exists = await user_repository.check_exists(username='nonexistingusername', session=session)
    assert not exists
