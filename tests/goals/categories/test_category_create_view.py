import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Category
from factories import BoardFactory


class TestCategoryCreateView:
    @pytest.mark.django_db
    def test_category_create_view(self, login_client_with_user, users_board):
        client, user = login_client_with_user

        data = {
            'title': 'Test title',
            'board': users_board.id,
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
        assert new_category.board == users_board, 'Неверная доска у категории'
        assert new_category.created is not None, 'Нет даты создания'
        assert new_category.updated is not None, 'Нет даты обновления'

    @pytest.mark.django_db
    def test_category_create_view_errors(self, client_and_board, big_pk):
        client, board = client_and_board
        not_user_board = BoardFactory.create()

        # Обращение без данных
        response_3 = client.post(
            '/goals/goal_category/create',
        )
        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с пустой строкой или с пустым значением
        data_2_1 = {
            'title': '',
            'board': ''
        }
        data_2_2 = {
            'title': None,
            'board': None
        }
        for data in (data_2_1, data_2_2):
            response_2 = client.post(
                '/goals/goal_category/create',
                data=data,
                content_type='application/json'
            )
            assert response_2.status_code == HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с несуществующей или удаленной доской
        board.is_deleted = True
        board.save()
        data_3_1 = {
            'title': 'Test title',
            'board': big_pk,
        }
        response_3_1 = client.post(
            '/goals/goal_category/create',
            data=data_3_1,
            content_type='application/json'
        )
        assert response_3_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        data_3_2 = {
            'title': 'Test title',
            'board': board.id,
        }
        response_3_2 = client.post(
            '/goals/goal_category/create',
            data=data_3_2,
            content_type='application/json'
        )
        assert response_3_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_3_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение без авторизации
        client.logout()
        data_4 = {
            'title': 'Test title',
            'board': not_user_board.id,
        }
        response_4 = client.post(
            '/goals/goal_category/create',
            data=data_4,
            content_type='application/json'
        )
        assert response_4.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_403_FORBIDDEN}'
