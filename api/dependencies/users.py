from sqlalchemy.ext.asyncio import async_sessionmaker

from repositories.sqlalchemy.common import engine
from repositories.sqlalchemy.users.repositories import SQLAlchemyUserRepository


def create_session():
    return async_sessionmaker(engine, expire_on_commit=False)()


def create_user_repository():
    return SQLAlchemyUserRepository()
