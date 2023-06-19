from factory import Factory, SubFactory
from factory.faker import Faker
from models.api_keys import APIKey

from models.users import User


class UserFactory(Factory):
    username = Faker('first_name')
    date_joined = Faker('past_date')

    class Meta:
        model = User


class APIKeyFactory(Factory):
    user = SubFactory(UserFactory)
    key = Faker('uuid4')
    user_id = Faker('pyint')
    last_used = None
    is_banned = False
    created_at = Faker('past_date')

    class Meta:
        model = APIKey
