from factory import Factory
from factory.faker import Faker

from models.users import User



class UserFactory(Factory):
    username = Faker('first_name')
    date_joined = Faker('past_date')

    class Meta:
        model = User
