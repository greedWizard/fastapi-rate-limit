import pathlib

import environ
from pydantic import BaseSettings


BASE_DIR = pathlib.Path(__file__).parent.parent


env = environ.Env()
env.__class__.read_env(BASE_DIR / '.env')


class ProjectSettings(BaseSettings):
    BASE_DIR: str = str(BASE_DIR)
    postgres_host: str = env('MONGO_HOST')
    postgres_port: int = env('MONGO_PORT', int)
    postgres_db: str = env('MONGO_USERS_DB', default='users-db')


settings = ProjectSettings()
