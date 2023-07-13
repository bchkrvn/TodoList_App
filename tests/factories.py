import datetime

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from core.models import User
from goals.models import Category, Goal, Comment, Board, BoardParticipant


class UniqueFaker(Faker):
    def evaluate(self, instance, step, extra):
        locale = extra.pop('locale')
        subfaker = self._get_faker(locale)
        unique_proxy = subfaker.unique
        return unique_proxy.format(self.provider, **extra)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = UniqueFaker('email')
    username = UniqueFaker('name')


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('name')


class BoardParticipantFactory(DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = SubFactory(BoardFactory)
    user = SubFactory(UserFactory)
    role = BoardParticipant.Role.reader


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = SubFactory(UserFactory)
    title = Faker('name')
    board = SubFactory(BoardFactory)


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    title = UniqueFaker('name')
    description = UniqueFaker('sentence', nb_words=10)
    category = SubFactory(CategoryFactory)
    user = SubFactory(UserFactory)
    priority = Goal.PriorityChoices.low
    status = Goal.StatusChoices.to_do
    due_date = datetime.date.today()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    user = SubFactory(UserFactory)
    goal = SubFactory(GoalFactory)
    text = Faker('sentence', nb_words=20)
