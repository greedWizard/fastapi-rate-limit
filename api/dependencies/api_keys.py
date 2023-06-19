from repositories.sqlalchemy.api_keys.repositories import APIKeySQLAlchemyRepository


def create_api_key_repository():
    return APIKeySQLAlchemyRepository()
