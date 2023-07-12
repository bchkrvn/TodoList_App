import pytest
import datetime
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.goals_serializers import GoalSerializer
from factories import CategoryFactory, GoalFactory
from goals.models import Goal


class TestGoalUpdateView:
    @pytest.mark.django_db
    def test_goal_update_view(self, client_and_goal):
        client, goal = client_and_goal
        new_category = CategoryFactory(user=goal.user)

        data = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': Goal.StatusChoices.in_progress,
            'status': Goal.PriorityChoices.high,
            'category': new_category.pk,
        }
        response = client.put(
            f'/goals/goal/{goal.pk}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'

        data['due_date'] = datetime.date.fromisoformat(data['due_date'])
        data['category'] = new_category
        goal.refresh_from_db()
        for field, value in data.items():
            assert getattr(goal, field) == value, f'Неверное значение поля {field}'

        assert goal.updated > goal.created, 'Время обновления раньше времени создания'
        assert response.data == GoalSerializer(goal).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_goal_update_view_errors(self, client_and_goal):
        client, goal = client_and_goal
        not_users_category = CategoryFactory.create()
        not_user_goal = GoalFactory.create()

        # Обращение без данных
        response_2 = client.put(
            f'/goals/goal/{goal.pk}'
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение не к своей цели
        data_3 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': Goal.StatusChoices.in_progress,
            'status': Goal.PriorityChoices.high,
            'category': not_user_goal.category.pk,
        }
        response_3 = client.put(
            f'/goals/goal/{not_user_goal.pk}',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей или к не своей категории, с неправильными данными
        data_4_1 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': 'дата',
            'priority': 10000,
            'status': 10000,
            'category': 1000000000,
        }
        data_4_2 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-02-31',
            'priority': 'значение',
            'status': 'значение',
            'category': not_users_category.pk,
        }
        for data_6 in (data_4_1, data_4_2):
            response_4 = client.put(
                f'/goals/goal/{goal.pk}',
                data=data_6,
                content_type='application/json'
            )
            assert response_4.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_4.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с пустой строкой или None
        data_5_1 = {
            'title': '',
            'description': '',
            'due_date': '',
            'priority': '',
            'status': '',
            'category': '',
        }
        data_5_2 = {
            'title': None,
            'description': None,
            'due_date': None,
            'priority': None,
            'status': None,
            'category': None,
        }

        for data_6 in [data_5_1, data_5_2]:
            response_5 = client.put(
                f'/goals/goal/{goal.pk}',
                data=data_6,
                content_type='application/json'
            )
            assert response_5.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_5.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение к удаленной категории
        new_category = CategoryFactory(user=goal.user, is_deleted=True)
        data_6 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': Goal.StatusChoices.in_progress,
            'status': Goal.PriorityChoices.high,
            'category': new_category.pk,
        }
        response_6 = client.put(
            f'/goals/goal/{goal.pk}',
            data=data_6,
            content_type='application/json'
        )
        assert response_6.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_6.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert {'category', } == set(response_6.data.keys()), 'Возвращаются не те ошибки'

        # Обращение неавторизованного пользователя
        client.logout()
        data_1 = {
            'title': 'Test title',
            'description': 'Test description',
            'due_date': '2023-01-01',
            'priority': Goal.StatusChoices.in_progress,
            'status': Goal.PriorityChoices.high,
            'category': goal.category.pk,
        }
        response_1 = client.put(
            f'/goals/goal/{goal.pk}',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
