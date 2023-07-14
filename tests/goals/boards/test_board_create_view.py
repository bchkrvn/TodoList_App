import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Board, BoardParticipant
from goals.serializers.board_serializer import BoardCreateSerializer


class TestBoardCreateView:
    @pytest.mark.django_db
    def test_board_create_view(self, login_client_with_user):
        client, user = login_client_with_user

        data = {
            'title': 'Test title',
        }
        response = client.post(
            '/goals/board/create',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == HTTP_201_CREATED, \
            f'Возвращается код {response.status_code} вместо {HTTP_201_CREATED}'

        board = Board.objects.last()
        assert response.data == BoardCreateSerializer(board).data, 'Возвращаются неверные данные'

        board_owner = BoardParticipant.objects.last()
        assert board_owner.user == user, 'Неверный пользователь'
        assert board_owner.board == board, 'Неверная доска'
        assert board_owner.role == BoardParticipant.Role.owner, 'Неверная роль пользователя'

    @pytest.mark.django_db
    def test_board_create_view_errors(self, login_client_with_user):
        client, user = login_client_with_user

        # Обращение без данных
        response_1 = client.post(
            '/goals/board/create',
        )
        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается код {response_1.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение c None или пустой строкой
        data_2_1 = {
            'title': None,
        }
        data_2_2 = {
            'title': '',
        }

        for data in (data_2_1, data_2_2):
            response_2 = client.post(
                '/goals/board/create',
                data=data,
                content_type='application/json'
            )

            assert response_2.status_code == HTTP_400_BAD_REQUEST, \
                f'Возвращается код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение неавторизованного пользователя
        client.logout()
        data_3 = {
            'title': 'Test title',
        }

        response_3 = client.post(
            '/goals/board/create',
            data=data_3,
            content_type='application/json'
        )

        assert response_3.status_code == HTTP_403_FORBIDDEN, \
            f'Возвращается код {response_3.status_code} вместо {HTTP_403_FORBIDDEN}'
