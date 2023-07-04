import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from factories import GoalFactory, CategoryFactory


class TestGoalListView:
    COUNT = 5
    LIMIT = 300

    @pytest.fixture
    def get_data(self, login_client_with_user):
        client, user = login_client_with_user
        response_keys = {'count', 'next', 'previous', 'results'}
        category = CategoryFactory.create(user=user)
        goals = GoalFactory.create_batch(category=category, user=user, size=self.COUNT)
        not_user_category = CategoryFactory.create()
        not_user_goals = GoalFactory.create_batch(category=not_user_category, size=self.COUNT)
        return client, response_keys, category, goals

    @pytest.mark.django_db
    def test_goal_list_view(self, get_data):
        client, response_keys, category, goals = get_data
        response = client.get(
            f'/goals/goal/list',
            {"limit": self.LIMIT}
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'
        assert response_keys == set(response.data.keys()), 'Ключи ответа не сходятся'
        assert response.data['count'] == self.COUNT, 'Неверное количество записей'
        assert len(response.data['results']) == self.COUNT, 'Вернулось не то количество элементов'

    @pytest.mark.django_db
    def test_category_list_view_errors(self, client):
        # Неавторизованный пользователь
        response = client.get(
            f'/goals/goal/list',
            {"limit": self.LIMIT}
        )
        assert response.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'
