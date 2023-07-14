import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from factories import GoalFactory, CategoryFactory


class TestGoalListView:
    COUNT = 5
    LIMIT = 300

    @pytest.fixture
    def get_data(self, client_and_category):
        client, category = client_and_category
        goals = GoalFactory.create_batch(category=category, user=category.user, size=self.COUNT)
        not_user_goals = GoalFactory.create_batch(size=self.COUNT)
        return client, goals

    @pytest.mark.django_db
    def test_goal_list_view(self, get_data, response_keys):
        client, goals = get_data
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
    def test_goal_list_view_errors(self, client):
        # Неавторизованный пользователь
        response = client.get(
            f'/goals/goal/list',
            {"limit": self.LIMIT}
        )
        assert response.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'
