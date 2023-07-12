import pytest
from rest_framework.status import HTTP_200_OK

from factories import BoardFactory, BoardParticipantFactory
from goals.models import BoardParticipant
from goals.serializers.board_serializer import BoardListSerializer


class TestBoardListView:
    COUNT = 5
    PAGE_SIZE = 2

    @pytest.fixture
    @pytest.mark.django_db
    def get_boards(self, login_client_with_user):
        client, user = login_client_with_user
        boards = BoardFactory.create_batch(size=self.COUNT)
        not_user_boards = BoardFactory.create_batch(size=self.PAGE_SIZE)
        boards.sort(key=lambda b: b.title)
        boards_owner = [BoardParticipantFactory.create(board=board, user=user, role=BoardParticipant.Role.owner)
                        for board in boards]

        return client, boards

    @pytest.mark.django_db
    def test_board_list_view_first_page(self, get_boards, response_keys):
        client, boards = get_boards

        response = client.get(
            f'/goals/board/list',
            {"limit": self.PAGE_SIZE}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == BoardListSerializer(boards[:self.PAGE_SIZE], many=True).data, \
            f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_board_list_view_middle_page(self, get_boards, response_keys):
        client, boards = get_boards

        response = client.get(
            f'/goals/board/list',
            {"limit": self.PAGE_SIZE, 'offset': self.PAGE_SIZE}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is not None, 'Нет ссылки на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == BoardListSerializer(boards[self.PAGE_SIZE:self.PAGE_SIZE * 2],
                                                               many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_board_list_view_last_page(self, get_boards, response_keys):
        client, boards = get_boards
        response = client.get(
            f'/goals/board/list',
            {"limit": self.PAGE_SIZE, 'offset': self.PAGE_SIZE * (self.COUNT // self.PAGE_SIZE)}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is None, 'Есть ссылка на следующую страницу'
        assert response.data['previous'] is not None, 'Нет ссылки на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.COUNT % self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == BoardListSerializer(boards[-(self.COUNT % self.PAGE_SIZE):],
                                                               many=True).data, f'Вернулись неверные данные'
