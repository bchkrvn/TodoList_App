import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.goals_serializers import GoalSerializer
from factories import GoalFactory


class TestGoalRetrieveAPIView:
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
    def test_goal_retrieve_view_errors(self, client_and_goal, big_pk):
        client, goal = client_and_goal
        not_users_goal = GoalFactory.create()

        # Обращение не к своей цели или к несуществующей цели
        response_2 = client.get(
            f'/goals/goal/{not_users_goal.pk}'
        )
        assert response_2.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_2 = client.get(
            f'/goals/goal/{big_pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_1 = client.get(
            f'/goals/goal/{goal.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
