import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from factories import GoalFactory
from goals.models import Goal


class TestGoalDestroyView:
    @pytest.mark.django_db
    def test_goal_destroy_view(self, client_and_goal):
        client, goal = client_and_goal

        response = client.delete(
            f'/goals/goal/{goal.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        goal.refresh_from_db()
        assert goal.status == Goal.StatusChoices.archived, 'Цель не помечена как в архиве'

    @pytest.mark.django_db
    def test_goal_destroy_view_errors(self, client, client_and_goal):
        client, goal = client_and_goal
        not_users_goal = GoalFactory.create()

        # Обращение к чужой и несуществующей цели
        for pk in [not_users_goal.pk, 10000000000]:
            response_2 = client.delete(
                f'/goals/goal_category/{pk}',
            )
            assert response_2.status_code is HTTP_404_NOT_FOUND, \
                f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_1 = client.delete(
            f'/goals/goal/{goal.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
