import pytest
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from factories import CommentFactory
from goals.models import Comment


class TestCommentDestroyView:
    @pytest.mark.django_db
    def test_comment_destroy_view(self, client_and_comment):
        client, comment = client_and_comment

        response = client.delete(
            f'/goals/goal_comment/{comment.pk}'
        )
        assert response.status_code is HTTP_204_NO_CONTENT, \
            f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'

        assert not Comment.objects.filter(pk=comment.pk).exists(), 'Комментарий остался в БД'

    @pytest.mark.django_db
    def test_comment_destroy_view_errors(self, client, users_comment, user_with_password):
        user, password = user_with_password
        comment = users_comment
        not_users_comment = CommentFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.delete(
            f'/goals/goal_comment/{comment.pk}',
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к чужому и несуществующему комментарию
        client.login(username=user.username, password=password)
        for pk in [not_users_comment.pk, 10000000000]:
            response_2 = client.delete(
                f'/goals/goal_comment/{pk}',
            )
            assert response_2.status_code is HTTP_404_NOT_FOUND, \
                f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'
