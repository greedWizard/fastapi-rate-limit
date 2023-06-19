from faker import Faker
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette import status


@pytest.mark.asyncio
async def test_user_create(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for('create_user_handler')
    response = client.post(
        url,
        json={
            'username': '12',
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_user_create(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_user_handler')
    response = client.post(
        url,
        json={
            'username': faker.first_name() * 2,
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
