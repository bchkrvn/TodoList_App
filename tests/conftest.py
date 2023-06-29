import pytest
from pytest_factoryboy import register

import factories

register(factories.UserFactory)


@pytest.fixture
def password():
    return 'f306e7b84a00240677664f503e4d77a60ccf848d746c475add39cea6fb3995a8'


@pytest.fixture
def simple_password():
    return '1111'


@pytest.fixture
@pytest.mark.django_db
def user_with_password(password):
    user = factories.UserFactory()
    user.set_password(password)
    user.save()
    return user, password
