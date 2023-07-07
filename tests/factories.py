import datetime

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from core.models import User
from goals.models import Category, Goal, Comment, StatusChoices, PriorityChoices


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    username = Faker('name')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = SubFactory(UserFactory)
    title = Faker('name')


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    title = Faker('name')
    description = Faker('sentence', nb_words=10)
    category = SubFactory(CategoryFactory)
    user = SubFactory(UserFactory)
    priority = PriorityChoices.low
    status = StatusChoices.to_do
    due_date = datetime.date.today()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    user = SubFactory(UserFactory)
    goal = SubFactory(GoalFactory)
    text = Faker('sentence', nb_words=20)
