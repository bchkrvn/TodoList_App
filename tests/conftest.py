import pytest
from pytest_factoryboy import register

from goals.models import BoardParticipant
import factories

register(factories.UserFactory)
register(factories.CategoryFactory)
register(factories.GoalFactory)
register(factories.CommentFactory)
register(factories.BoardFactory)
register(factories.BoardParticipantFactory)


@pytest.fixture
def password():
    return 'f306e7b84a00240677664f503e4d77a60ccf848d746c475add39cea6fb3995a8'


@pytest.fixture
def response_keys():
    return {'count', 'next', 'previous', 'results'}


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
def users_board(user_with_password, board):
    user, _ = user_with_password
    board_owner = factories.BoardParticipantFactory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    return board


@pytest.fixture
@pytest.mark.django_db
def client_and_board(login_client_with_user, board):
    client, user = login_client_with_user
    board_owner = factories.BoardParticipantFactory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    return client, board


@pytest.fixture
@pytest.mark.django_db
def client_and_category(login_client_with_user, users_board):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user, board=users_board)
    not_user_categories = factories.CategoryFactory.create_batch(5)
    return client, category


@pytest.fixture
@pytest.mark.django_db
def client_and_goal(login_client_with_user, users_board):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user, board=users_board)
    goal = factories.GoalFactory.create(user=user, category=category)
    not_user_goals = factories.GoalFactory.create_batch(5)
    return client, goal


@pytest.fixture
@pytest.mark.django_db
def client_and_comment(login_client_with_user, users_board):
    client, user = login_client_with_user
    category = factories.CategoryFactory.create(user=user, board=users_board)
    goal = factories.GoalFactory.create(user=user, category=category)
    comment = factories.CommentFactory.create(user=user, goal=goal)
    not_user_comments = factories.CommentFactory.create_batch(5)
    return client, comment


@pytest.fixture
@pytest.mark.django_db
def users_comment(user_with_password, users_board):
    user, password = user_with_password
    category = factories.CategoryFactory.create(user=user, board=users_board)
    goal = factories.GoalFactory.create(user=user, category=category)
    comment = factories.CommentFactory.create(user=user, goal=goal)
    return comment


@pytest.fixture
@pytest.mark.django_db
def boards_owner_writer_reader_alien():
    general_board = factories.BoardFactory.create()
    owner, writer, reader, alien = factories.UserFactory.create_batch(size=4)

    factories.BoardParticipantFactory.create(user=owner, board=general_board, role=BoardParticipant.Role.owner)
    factories.BoardParticipantFactory.create(user=writer, board=general_board, role=BoardParticipant.Role.writer)
    factories.BoardParticipantFactory.create(user=reader, board=general_board, role=BoardParticipant.Role.reader)

    personal_board = factories.BoardFactory.create()
    factories.BoardParticipantFactory.create(user=owner, board=personal_board, role=BoardParticipant.Role.owner)

    return general_board, personal_board, owner, writer, reader, alien


@pytest.fixture
@pytest.mark.django_db
def one_board_owner_writer_reader_alien():
    board = factories.BoardFactory.create()
    owner, writer, reader, alien = factories.UserFactory.create_batch(size=4)

    factories.BoardParticipantFactory.create(user=owner, board=board, role=BoardParticipant.Role.owner)
    factories.BoardParticipantFactory.create(user=writer, board=board, role=BoardParticipant.Role.writer)
    factories.BoardParticipantFactory.create(user=reader, board=board, role=BoardParticipant.Role.reader)

    return board, owner, writer, reader, alien
