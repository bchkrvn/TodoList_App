import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from factories import CategoryFactory, GoalFactory, BoardFactory
from goals.models import Goal


class TestBoardDestroyView:
    SIZE = 2

    @pytest.mark.django_db
    def test_board_destroy_view(self, client_and_board, user_with_password):
        user, _ = user_with_password
        client, board = client_and_board
        categories = CategoryFactory.create_batch(user=user, board=board, size=self.SIZE)
        goals = [GoalFactory.create_batch(size=self.SIZE, category=category) for category in categories]

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
                goal.refresh_from_db()
                assert goal.status == Goal.StatusChoices.archived, 'Цель не помечена как в архиве после удаления доски'

    @pytest.mark.django_db
    def test_board_destroy_view_errors(self, client_and_board, user_with_password, big_pk):
        client, board = client_and_board
        not_users_board = BoardFactory.create()

        # Обращение к чужой и несуществующей доске
        response_1 = client.delete(
            f'/goals/board/{not_users_board.pk}',
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_2 = client.delete(
            f'/goals/board/{big_pk}',
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к удаленной доске
        board.is_deleted = True
        board.save()
        response_3 = client.delete(
            f'/goals/board/{board.pk}',
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_4 = client.delete(
            f'/goals/board/{board.pk}',
        )
        assert response_4.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_403_FORBIDDEN}'
