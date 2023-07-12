import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from factories import CategoryFactory, GoalFactory, BoardFactory
from goals.models import Goal


class TestBoardDestroyView:
    @pytest.mark.django_db
    def test_board_destroy_view(self, client_and_board, user_with_password):
        user, _ = user_with_password
        client, board = client_and_board
        categories = CategoryFactory.create_batch(user=user, board=board, size=2)
        [GoalFactory.create_batch(size=2, category=category) for category in categories]

        response = client.delete(
            f'/goals/board/{board.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        board.refresh_from_db()
        assert board.is_deleted, 'Доска не помечена как удаленная'

        for category in categories:
            category.refresh_from_db()
            assert category.is_deleted, 'Категория не помечена как удаленная'
            for goal in category.goals.all():
                assert goal.status == Goal.StatusChoices.archived, 'Цель не помечена как в архиве после удаления доски'

    @pytest.mark.django_db
    def test_board_destroy_view_errors(self, client_and_board, user_with_password):
        user, _ = user_with_password
        client, board = client_and_board
        not_users_board = BoardFactory.create()

        # Обращение к чужой и несуществующей доске
        response_2 = client.delete(
            f'/goals/board/{not_users_board.pk}',
        )
        assert response_2.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_2 = client.delete(
            f'/goals/board/{10000000000}',
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_1 = client.delete(
            f'/goals/board/{board.pk}',
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
