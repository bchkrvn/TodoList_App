import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from factories import GoalFactory
from goals.models import StatusChoices


class TestGoalDestroyView:
    @pytest.mark.django_db
    def test_goal_destroy_view(self, login_client_with_user):
        client, user = login_client_with_user
        goal = GoalFactory.create(user=user)

        response = client.delete(
            f'/goals/goal/{goal.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        goal.refresh_from_db()
        assert goal.status == StatusChoices.archived, 'Цель не помечена как в архиве'

    @pytest.mark.django_db
    def test_goal_destroy_view_errors(self, client, user_with_password):
        user, password = user_with_password
        goal = GoalFactory.create(user=user)
        not_users_goal = GoalFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.delete(
            f'/goals/goal/{goal.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к чужой и несуществующей цели
        client.login(username=user.username, password=password)
        for pk in [not_users_goal.pk, 10000000000]:
            response_2 = client.delete(
                f'/goals/goal_category/{pk}',
            )
            assert response_2.status_code is HTTP_404_NOT_FOUND, \
                f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'
