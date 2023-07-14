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
    def test_category_retrieve_view_errors(self, client_and_category, big_pk):
        client, category = client_and_category
        not_users_category = CategoryFactory.create()

        # Обращение не к своей категории
        response_1 = client.get(
            f'/goals/goal_category/{not_users_category.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей категории
        response_2 = client.get(
            f'/goals/goal_category/{big_pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к удаленной категории
        category.is_deleted = True
        category.save()
        response_3 = client.get(
            f'/goals/goal_category/{category.pk}'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_4 = client.get(
            f'/goals/goal_category/{not_users_category.pk}'
        )
        assert response_4.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_403_FORBIDDEN}'
