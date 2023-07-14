import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.board_serializer import BoardSerializer
from factories import BoardFactory


class TestBoardUpdateView:
    @pytest.mark.django_db
    def test_board_update_view(self, client_and_board):
        client, board = client_and_board

        data = {
            'title': 'new_title',
            'participants': [],
        }
        response = client.put(
            f'/goals/board/{board.pk}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data['title'] == data['title'], 'Название не обновилось'
        assert response.data['updated'] != response.data['created'], 'Время обновления не установилось'
        board.refresh_from_db()
        assert board.updated > board.created, 'Время обновления раньше времени создания'
        assert response.data == BoardSerializer(board).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_update_view_errors(self, client_and_board, big_pk):
        client, board = client_and_board
        not_users_board = BoardFactory.create()

        # Обращение без данных
        response_2 = client.put(
            f'/goals/board/{board.pk}'
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение не к своей доске
        data_3 = {
            'title': 'new_title',
            'participants': [],
        }
        response_3 = client.put(
            f'/goals/board/{not_users_board.pk}',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей доске
        data_4 = {
            'title': 'new_title',
            'participants': [],
        }
        response_4 = client.put(
            f'/goals/board/{big_pk}',
            data=data_4,
            content_type='application/json'
        )
        assert response_4.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение с пустой строкой или None
        data_5_1 = {
            'title': '',
            'participants': [],
        }
        data_5_2 = {
            'title': None,
            'participants': [],
        }

        for data in [data_5_1, data_5_2]:
            response_5 = client.put(
                f'/goals/board/{board.pk}',
                data=data,
                content_type='application/json'
            )
            assert response_5.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_5.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение к удаленной доске
        board.is_deleted = True
        board.save()
        data_6 = {
            'title': 'new_title',
            'participants': [],
        }
        response_6 = client.put(
            f'/goals/board/{board.pk}',
            data=data_6,
            content_type='application/json'
        )
        assert response_6.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_6.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        data_1 = {
            'title': 'new_title',
            'participants': [],
        }
        response_1 = client.put(
            f'/goals/board/{board.pk}',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
