from distutils.util import strtobool
import pathlib

import environ
from pydantic import BaseSettings


BASE_DIR = pathlib.Path(__file__).parent.parent


env = environ.Env()
env.__class__.read_env(BASE_DIR / '.env')


class ProjectSettings(BaseSettings):
    debug: str = env('DEBUG', strtobool, default=False)
    base_dir: str = str(BASE_DIR)
    postgres_host: str = env('POSTGRES_HOST')
    postgres_port: int = env('POSTGRES_PORT', int)
    postgres_db: str = env('POSTGRES_DB')
    postgres_user: str = env('POSTGRES_USER')
    postgres_password: str = env('POSTGRES_PASSWORD')
    db_connection_string: str = (
        'postgresql+asyncpg://'
        f'{postgres_user}:{postgres_password}'
        f'@{postgres_host}/{postgres_db}'
    )
    minimal_username_length: int = 6


settings = ProjectSettings()
