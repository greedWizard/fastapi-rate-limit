import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app import create_app
from api.dependencies.users import create_session, create_user_repository

from tests.conftest import *
from tests.fixtures import FakeSession  # no qa


@pytest.fixture
def app(user_repository: FakeUserRepository):
    app = create_app()
    app.dependency_overrides[create_session] = lambda: FakeSession()
    app.dependency_overrides[create_user_repository] = lambda: user_repository

    yield app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
