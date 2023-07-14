import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from factories import CategoryFactory, GoalFactory
from goals.models import Goal


class TestCategoryDestroyView:
    SIZE = 2

    @pytest.mark.django_db
    def test_category_destroy_view(self, login_client_with_user, users_board):
        client, user = login_client_with_user
        category = CategoryFactory.create(user=user, board=users_board)
        GoalFactory.create_batch(size=self.SIZE, category=category)

        response = client.delete(
            f'/goals/goal_category/{category.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        category.refresh_from_db()
        assert category.is_deleted, 'Категория не помечена как удаленная'
        for goal in category.goals.all():
            assert goal.status == Goal.StatusChoices.archived, 'Цель не помечена как в архиве после удаления категории'

    @pytest.mark.django_db
    def test_category_destroy_view_errors(self, client_and_category, big_pk):
        client, category = client_and_category
        not_users_category = CategoryFactory.create()

        # Обращение к чужой и несуществующей категории
        response_1_1 = client.delete(
            f'/goals/goal_category/{not_users_category.pk}',
        )
        assert response_1_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_1_2 = client.delete(
            f'/goals/goal_category/{big_pk}',
        )
        assert response_1_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_1_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к удаленной категории
        category.is_deleted = True
        category.save()
        response_3 = client.delete(
            f'/goals/goal_category/{category.pk}',
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_4 = client.delete(
            f'/goals/goal_category/{not_users_category.pk}',
        )
        assert response_4.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_403_FORBIDDEN}'
