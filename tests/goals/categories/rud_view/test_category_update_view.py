import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.categorises_serializers import CategorySerializer
from factories import CategoryFactory


class TestCategoryUpdateView:
    @pytest.mark.django_db
    def test_category_update_view(self, client_and_category):
        client, category = client_and_category

        data = {
            'title': 'new_title'
        }
        response = client.put(
            f'/goals/goal_category/{category.pk}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data['title'] == data['title'], 'Название не обновилось'
        assert response.data['updated'] != response.data['created'], 'Время обновления не установилось'
        category.refresh_from_db()
        assert category.updated > category.created, 'Время обновления раньше времени создания'
        assert response.data == CategorySerializer(category).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_update_view_errors(self, client_and_category, big_pk):
        client, category = client_and_category
        not_users_category = CategoryFactory.create()

        # Обращение без данных
        response_1 = client.put(
            f'/goals/goal_category/{category.pk}'
        )
        assert response_1.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение не к своей категории
        data_2 = {
            'title': 'new_title'
        }
        response_2 = client.put(
            f'/goals/goal_category/{not_users_category.pk}',
            data=data_2,
            content_type='application/json'
        )
        assert response_2.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей категории
        data_3 = {
            'title': 'new_title'
        }
        response_3 = client.put(
            f'/goals/goal_category/{big_pk}',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение с пустой строкой или None
        data_4_1 = {
            'title': ''
        }
        data_4_2 = {
            'title': None
        }

        for data in [data_4_1, data_4_2]:
            response_4 = client.put(
                f'/goals/goal_category/{category.pk}',
                data=data,
                content_type='application/json'
            )
            assert response_4.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_4.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение к удаленной категории
        category.is_deleted = True
        category.save()
        data_5 = {
            'title': 'new_title'
        }
        response_5 = client.put(
            f'/goals/goal_category/{category.pk}',
            data=data_5,
            content_type='application/json'
        )
        assert response_5.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_5.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        data_6 = {
            'title': 'new_title'
        }
        response_6 = client.put(
            f'/goals/goal_category/{not_users_category.pk}',
            data=data_6,
            content_type='application/json'
        )
        assert response_6.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_6.status_code} вместо {HTTP_403_FORBIDDEN}'
