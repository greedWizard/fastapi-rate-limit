import pytest

from tests.fixtures import FakeUserRepository


@pytest.fixture
def user_repository():
    return FakeUserRepository()
