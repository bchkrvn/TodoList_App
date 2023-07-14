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
    def test_comment_destroy_view_errors(self, client_and_comment, big_pk):
        client, comment = client_and_comment
        not_users_comment = CommentFactory.create()

        # Обращение к чужому и несуществующему комментарию
        response_2 = client.delete(
            f'/goals/goal_comment/{not_users_comment.pk}',
        )
        assert response_2.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_3 = client.delete(
            f'/goals/goal_comment/{big_pk}',
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение неавторизованного пользователя
        client.logout()
        response_1 = client.delete(
            f'/goals/goal_comment/{comment.pk}',
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
