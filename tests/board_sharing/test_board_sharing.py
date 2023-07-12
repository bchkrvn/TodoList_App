import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from goals.serializers.board_serializer import BoardListSerializer
from goals.models import BoardParticipant
from factories import UserFactory


class TestBoardSharing:
    PAGE = 10
    COUNT = 1
    OWNER_COUNT = 2
    OWNER_INDEX = 3
    ALIEN_INDEX = 0

    @pytest.mark.django_db
    def test_board_sharing(self, client_and_board, user_with_password):
        owner, _ = user_with_password
        client, board = client_and_board
        writer, reader = UserFactory.create_batch(size=2)
        data = {
            'title': board.title,
            'participants': [{'user': writer.username, 'role': BoardParticipant.Role.writer},
                             {'user': reader.username, 'role': BoardParticipant.Role.reader}, ]
        }
        response = client.put(
            f'/goals/board/{board.pk}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'

        board.refresh_from_db()
        assert len(board.participants.all()) == 3, 'Не у всех есть доступ'

        assert board.participants.filter(user=owner, role=BoardParticipant.Role.owner).exists(), f'Нет владельца'
        assert board.participants.filter(user=writer, role=BoardParticipant.Role.writer).exists(), f'Нет редактора'
        assert board.participants.filter(user=reader, role=BoardParticipant.Role.reader).exists(), f'Нет читателя'

    @pytest.mark.django_db
    def test_board_sharing_list(self, boards_owner_writer_reader_alien, client):
        general_board, personal_board, owner, writer, reader, alien = boards_owner_writer_reader_alien
        boards = sorted([general_board, personal_board], key=lambda b: b.title)

        for i, user in enumerate([alien, writer, reader, owner]):
            client.force_login(user)
            response = client.get(
                '/goals/board/list',
                data={'limit': self.PAGE}
            )

            assert response.status_code is HTTP_200_OK, \
                f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'

            if i == self.OWNER_INDEX:
                assert response.data['count'] == self.OWNER_COUNT, 'Неверное количество записей для владельца'
                assert response.data['results'] == BoardListSerializer(boards,
                                                                       many=True).data, \
                    f'Вернулись неверные данные для владельца'

            elif i == self.ALIEN_INDEX:
                assert response.data['count'] == 0, 'Есть данные у не участника'
            else:
                assert response.data['count'] == self.COUNT, f'Неверное количество записей для i={i}'
                assert response.data['results'] == BoardListSerializer([general_board], many=True).data, \
                    f'Вернулись неверные данные для i={i}'

    @pytest.mark.django_db
    def test_board_sharing_edit(self, boards_owner_writer_reader_alien, client):
        general_board, personal_board, owner, writer, reader, alien = boards_owner_writer_reader_alien

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'title': f'title from {i} user',
                'participants': []
            }
            response = client.put(
                f'/goals/board/{general_board.pk}',
                data=data,
                content_type='application/json'
            )

            if i == self.OWNER_INDEX:
                assert response.status_code is HTTP_200_OK, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
                general_board.refresh_from_db()
                assert len(general_board.participants.all()) == 1, 'Доступ не только у владельца'
            else:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

    @pytest.mark.django_db
    def test_board_sharing_delete(self, boards_owner_writer_reader_alien, client):
        general_board, personal_board, owner, writer, reader, alien = boards_owner_writer_reader_alien

        for i, user in enumerate([alien, writer, reader, owner]):
            client.force_login(user)
            response = client.delete(
                f'/goals/board/{general_board.pk}',
            )

            if i == self.OWNER_INDEX:
                assert response.status_code is HTTP_204_NO_CONTENT, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_204_NO_CONTENT}'
            else:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'
