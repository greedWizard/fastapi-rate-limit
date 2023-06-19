from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from common.settings import settings


meta = MetaData()

engine: AsyncEngine = create_async_engine(
    settings.db_connection_string,
    echo=True,
)
