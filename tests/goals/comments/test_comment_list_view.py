import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from factories import CommentFactory, GoalFactory, UserFactory
from goals.serializers.comments_serializers import CommentSerializer


class TestCommentListView:
    COUNT = 12
    PAGE_SIZE = 5

    @pytest.fixture
    @pytest.mark.django_db
    def get_data(self, client_and_goal):
        client, goal = client_and_goal
        comments = CommentFactory.create_batch(size=self.COUNT, user=goal.user, goal=goal)
        not_users_comments = CommentFactory.create_batch(size=self.COUNT)

        return client, comments, goal

    @pytest.mark.django_db
    def test_comments_list_view_first_page(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'goal': goal.pk}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        comments.sort(key=lambda c: c.created, reverse=True)
        assert response.data['results'] == CommentSerializer(comments[:self.PAGE_SIZE], many=True).data, \
            f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_comments_list_view_middle_page(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'offset': self.PAGE_SIZE, 'goal': goal.pk}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is not None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        comments.sort(key=lambda c: c.created, reverse=True)
        assert response.data['results'] == CommentSerializer(comments[self.PAGE_SIZE:self.PAGE_SIZE * 2],
                                                             many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_comments_list_view_last_page(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE,
             'offset': self.PAGE_SIZE * (self.COUNT // self.PAGE_SIZE),
             'goal': goal.pk}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is not None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(
            response.data['results']) == self.COUNT % self.PAGE_SIZE, 'Вернулось не то количество элементов'
        comments.sort(key=lambda c: c.created, reverse=True)
        assert response.data['results'] == CommentSerializer(comments[-(self.COUNT % self.PAGE_SIZE):],
                                                             many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_comments_list_view_ordering_created(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'goal': goal.pk, 'ordering': 'created'}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        comments.sort(key=lambda c: c.created)
        assert response.data['results'] == CommentSerializer(comments[:self.PAGE_SIZE], many=True).data, \
            f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_comments_list_view_ordering_last_updated(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'goal': goal.pk, 'ordering': 'created'}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        comments.sort(key=lambda c: c.updated)
        assert response.data['results'] == CommentSerializer(comments[:self.PAGE_SIZE], many=True).data, \
            f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_comments_list_view_errors(self, client, user):
        another_user = UserFactory.create()
        goal = GoalFactory.create(user=another_user)
        comments = CommentFactory.create_batch(size=self.COUNT, goal=goal, user=another_user)

        # Неавторизованный пользователь
        response_1 = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'goal': goal.pk}
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код  {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к комментариям чужой цели
        client.force_login(user)
        response_2 = client.get(
            f'/goals/goal_comment/list',
            {"limit": self.PAGE_SIZE, 'goal': goal.pk}
        )
        assert response_2.status_code is HTTP_200_OK, \
            f'Вернулся код  {response_2.status_code} вместо {HTTP_200_OK}'
        assert response_2.data['count'] == 0, 'Неверное количество записей'
        assert not response_2.data['results'], 'Не пустой список'
