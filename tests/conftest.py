import pytest
from pytest_factoryboy import register

import factories

register(factories.UserFactory)
register(factories.CategoryFactory)
register(factories.GoalFactory)
register(factories.CommentFactory)


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


@pytest.fixture
@pytest.mark.django_db
def login_client_with_user(user_with_password, client):
    user, password = user_with_password
    client.login(username=user.username, password=password)
    return client, user


@pytest.fixture
@pytest.mark.django_db
def client_and_category(login_client_with_user):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user)
    not_user_categories = factories.CategoryFactory.create_batch(5)
    return client, category


@pytest.fixture
@pytest.mark.django_db
def client_and_goal(login_client_with_user):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user)
    goal = factories.GoalFactory.create(user=user, category=category)
    not_user_goals = factories.GoalFactory.create_batch(5)
    return client, goal


@pytest.fixture
@pytest.mark.django_db
def client_and_comment(login_client_with_user):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user)
    goal = factories.GoalFactory.create(user=user, category=category)
    comment = factories.CommentFactory.create(user=user, goal=goal)
    not_user_comments = factories.CommentFactory.create_batch(5)
    return client, comment


@pytest.fixture
@pytest.mark.django_db
def users_comment(user_with_password):
    user, password = user_with_password
    category = factories.CategoryFactory.create(user=user)
    goal = factories.GoalFactory.create(user=user, category=category)
    comment = factories.CommentFactory.create(user=user, goal=goal)
    return comment
