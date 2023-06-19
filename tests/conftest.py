import pytest

from tests.fixtures import FakeAPIKeyRepository, FakeUserRepository


@pytest.fixture
def user_repository():
    return FakeUserRepository()


@pytest.fixture
def api_key_repository():
    return FakeAPIKeyRepository()
