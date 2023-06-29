from factory import Faker
from factory.django import DjangoModelFactory

from core.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    username = Faker('name')
