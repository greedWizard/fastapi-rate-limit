from fastapi import FastAPI

from common.settings import settings
from repositories.sqlalchemy.factories import init_database


def create_app(init_db: bool = True):
    app = FastAPI(
        title='FastAPI API Rate Limit App',
        debug=settings.debug,
        docs_url='/api/docs',
        redoc_url='/api/redocs',
    )

    if init_db:
        init_database()

    return app
