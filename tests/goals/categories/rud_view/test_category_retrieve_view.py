import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.categorises_serializers import CategorySerializer
from factories import CategoryFactory


class TestCategoryRetrieveAPIView:
    @pytest.mark.django_db
    def test_category_retrieve_view(self, client_and_category):
        client, category = client_and_category

        response = client.get(
            f'/goals/goal_category/{category.pk}'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data == CategorySerializer(category).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_retrieve_view_errors(self, client, user_with_password, users_board):
        user, password = user_with_password
        category = CategoryFactory.create(user=user, board=users_board)
        not_users_category = CategoryFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.get(
            f'/goals/goal_category/{category.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение не к своей категории
        client.login(username=user.username, password=password)
        response_2 = client.get(
            f'/goals/goal_category/{not_users_category.pk}'
        )
        assert response_2.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей категории
        response_3 = client.get(
            f'/goals/goal_category/100000000'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'
