import pytest
from factories import CategoryFactory
from goals.serializers.categorises_serializers import CategorySerializer
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


class TestCategoryListView:
    COUNT = 12
    PAGE_SIZE = 5

    @pytest.fixture
    def get_data(self, login_client_with_user, users_board):
        client, user = login_client_with_user
        response_keys = {'count', 'next', 'previous', 'results'}
        categories = CategoryFactory.create_batch(size=self.COUNT, user=user, board=users_board)
        categories.sort(key=lambda c: c.title)
        not_user_categories = CategoryFactory.create_batch(size=self.COUNT)
        return client, response_keys, categories

    @pytest.mark.django_db
    def test_category_list_view_first_page(self, get_data):
        client, response_keys, categories = get_data

        response = client.get(
            f'/goals/goal_category/list',
            {"limit": self.PAGE_SIZE}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == CategorySerializer(categories[:self.PAGE_SIZE], many=True).data, \
            f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_list_view_middle_page(self, get_data):
        client, response_keys, categories = get_data

        response = client.get(
            f'/goals/goal_category/list',
            {"limit": self.PAGE_SIZE, 'offset': self.PAGE_SIZE}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is not None, 'Нет ссылки на следующую страницу'
        assert response.data['previous'] is not None, 'Нет ссылки на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == CategorySerializer(categories[self.PAGE_SIZE:self.PAGE_SIZE * 2],
                                                              many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_list_view_last_page(self, get_data):
        client, response_keys, categories = get_data

        response = client.get(
            f'/goals/goal_category/list',
            {"limit": self.PAGE_SIZE, 'offset': self.PAGE_SIZE * (self.COUNT % self.PAGE_SIZE)}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is None, 'Есть ссылки на следующую страницу'
        assert response.data['previous'] is not None, 'Нет ссылки на предыдущую страницу'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.COUNT % self.PAGE_SIZE, 'Вернулось не то количество элементов'
        assert response.data['results'] == CategorySerializer(categories[-(self.COUNT % self.PAGE_SIZE):],
                                                              many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_list_view_search(self, get_data):
        client, response_keys, categories = get_data
        category = categories[0]
        response = client.get(
            f'/goals/goal_category/list',
            {"limit": self.PAGE_SIZE, 'search': category.title}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['next'] is None, 'Есть ссылки на следующую страницу'
        assert response.data['previous'] is None, 'Есть ссылка на предыдущую страницу'
        assert response.data['count'] == 1, 'Неверное количество записей'
        assert len(response.data['results']) == 1, 'Вернулось не то количество элементов'
        assert response.data['results'] == CategorySerializer([category], many=True).data, f'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_list_view_errors(self, client):
        # Неавторизованный пользователь
        response = client.get(
            f'/goals/goal_category/list',
            {"limit": self.PAGE_SIZE}
        )
        assert response.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'
