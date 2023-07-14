import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.board_serializer import BoardSerializer
from factories import BoardFactory


class TestBoardRetrieveAPIView:
    @pytest.mark.django_db
    def test_board_retrieve_view(self, client_and_board):
        client, board = client_and_board

        response = client.get(
            f'/goals/board/{board.pk}'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data == BoardSerializer(board).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_board_retrieve_view_errors(self, client_and_board, big_pk):
        client, board = client_and_board
        not_users_board = BoardFactory.create()

        # Обращение не к своей доске
        response_1 = client.get(
            f'/goals/board/{not_users_board.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к несуществующей доске
        response_2 = client.get(
            f'/goals/board/{big_pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к удаленной доске
        board.is_deleted = True
        board.save()
        response_2 = client.get(
            f'/goals/board/{board.pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_3 = client.get(
            f'/goals/board/{not_users_board.pk}'
        )
        assert response_3.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_403_FORBIDDEN}'
