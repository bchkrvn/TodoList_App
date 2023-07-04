import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Category


class TestCategoryCreateView:
    @pytest.mark.django_db
    def test_category_create_view(self, login_client_with_user):
        client, user = login_client_with_user

        data = {
            'title': 'Test title'
        }
        response = client.post(
            '/goals/goal_category/create',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_201_CREATED, \
            f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'

        new_category = Category.objects.last()
        assert new_category.title == data['title'], 'Неверное название у категории'
        assert new_category.user == user, 'Неверный автор у категории'
        assert new_category.created is not None, 'Нет даты создания'
        assert new_category.updated is not None, 'Нет даты обновления'

    @pytest.mark.django_db
    def test_category_create_view_errors(self, client, user_with_password):
        user, password = user_with_password
        # Обращение без авторизации
        data_1 = {
            'title': 'Test title'
        }
        response_1 = client.post(
            '/goals/goal_category/create',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение без данных
        client.login(username=user.username, password=password)
        response_2 = client.post(
            '/goals/goal_category/create',
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с пустой строкой
        data_3 = {
            'title': ''
        }
        response_3 = client.post(
            '/goals/goal_category/create',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert 'title' in response_3.data, 'Нет сообщения об ошибке title'
