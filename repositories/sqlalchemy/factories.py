from sqlalchemy.orm import registry
from models.api_keys import APIKey
from models.responses import Response
from models.users import User

from repositories.sqlalchemy.api_keys.tables import api_keys_table
from repositories.sqlalchemy.users.tables import users_table
from repositories.sqlalchemy.responses.tables import responses_table


def init_database():
    mapper_registry = registry()
    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(APIKey, api_keys_table)
    mapper_registry.map_imperatively(Response, responses_table)
