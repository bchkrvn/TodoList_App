import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.goals_serializers import GoalSerializer
from factories import GoalFactory


class TestCoalRetrieveAPIView:
    @pytest.mark.django_db
    def test_goal_retrieve_view(self, client_and_goal):
        client, goal = client_and_goal

        response = client.get(
            f'/goals/goal/{goal.pk}'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data == GoalSerializer(goal).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_goal_retrieve_view_errors(self, client, user_with_password):
        user, password = user_with_password
        goal = GoalFactory.create(user=user)
        not_users_goal = GoalFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.get(
            f'/goals/goal/{goal.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение не к своей категории
        client.login(username=user.username, password=password)
        response_2 = client.get(
            f'/goals/goal/{not_users_goal.pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к несуществующей категории
        response_3 = client.get(
            f'/goals/goal/100000000'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'
