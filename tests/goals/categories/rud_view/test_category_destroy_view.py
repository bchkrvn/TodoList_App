import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from factories import CategoryFactory, GoalFactory
from goals.models import StatusChoices


class TestCategoryDestroyView:
    @pytest.mark.django_db
    def test_category_destroy_view(self, login_client_with_user):
        client, user = login_client_with_user
        category = CategoryFactory.create(user=user)
        GoalFactory.create_batch(size=2, category=category)

        response = client.delete(
            f'/goals/goal_category/{category.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        category.refresh_from_db()
        assert category.is_deleted, 'Категория не помечена как удаленная'
        for goal in category.goals.all():
            assert goal.status == StatusChoices.archived, 'Цель не помечена как в архиве после удаления категории'

    @pytest.mark.django_db
    def test_category_destroy_view_errors(self, client, user_with_password):
        user, password = user_with_password
        category = CategoryFactory.create(user=user)
        not_users_category = CategoryFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.delete(
            f'/goals/goal_category/{category.pk}',
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к чужой и несуществующей категории
        client.login(username=user.username, password=password)
        for pk in [not_users_category.pk, 10000000000]:
            response_2 = client.delete(
                f'/goals/goal_category/{pk}',
            )
            assert response_2.status_code is HTTP_404_NOT_FOUND, \
                f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'