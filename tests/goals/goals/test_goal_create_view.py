import datetime

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from goals.models import Goal, StatusChoices, PriorityChoices
from goals.serializers.goals_serializers import GoalCreateSerializer
from factories import CategoryFactory


class TestGoalCreateView:
    @pytest.mark.django_db
    def test_goal_create_view(self, login_client_with_user):
        client, user = login_client_with_user
        category = CategoryFactory.create(user=user)

        data = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': StatusChoices.to_do,
            'status': PriorityChoices.low,
            'category': category.pk,
        }
        response = client.post(
            '/goals/goal/create',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_201_CREATED, \
            f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'

        data['category'] = category
        data['due_date'] = datetime.date.fromisoformat(data['due_date'])
        data['user'] = user

        new_goal = Goal.objects.last()
        for field, value in data.items():
            assert getattr(new_goal, field) == value, f'Неверное значение поля {field}'

        assert response.data == GoalCreateSerializer(new_goal).data, f'Возвращаются неверные данные'

    @pytest.mark.django_db
    def test_goal_create_view_errors(self, client, user_with_password):
        user, password = user_with_password
        category = CategoryFactory.create(user=user)
        not_user_category = CategoryFactory.create()

        # Обращение без авторизации
        data_1 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': 1,
            'status': 1,
            'category': category.pk,
        }
        response_1 = client.post(
            '/goals/goal/create',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение без данных
        client.login(username=user.username, password=password)
        response_2 = client.post(
            '/goals/goal/create',
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращения с пустыми данными
        data_3_1 = {
            'title': '',
            'description': '',
            'priority': '',
            'status': '',
            'category': '',
        }
        data_3_2 = {
            'title': None,
            'description': None,
            'priority': None,
            'status': None,
            'category': None,
        }
        for data in [data_3_1, data_3_2]:
            response_3 = client.post(
                '/goals/goal/create',
                data=data,
                content_type='application/json'
            )
            assert response_3.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'
            assert set(data.keys()) == set(response_3.data.keys()), 'Возвращаются не те ошибки'

        # Обращение к чужой категории с неправильным статусом и приоритетом
        data_4 = {
            'title': 'Test title',
            'description': 'Test description',
            'priority': 1000,
            'status': 1000,
            'category': not_user_category.pk,
        }
        response_4 = client.post(
            '/goals/goal/create',
            data=data_4,
            content_type='application/json'
        )
        assert response_4.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert {'priority', 'status', 'category'} == set(response_4.data.keys()), 'Возвращаются не те ошибки'

        # Обращение к удаленной категории
        category.is_deleted = True
        category.save()

        data = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': 1,
            'status': 1,
            'category': category.pk,
        }
        response_5 = client.post(
            '/goals/goal/create',
            data=data,
            content_type='application/json'
        )
        assert response_5.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_5.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert {'category', } == set(response_5.data.keys()), 'Возвращаются не те ошибки'
