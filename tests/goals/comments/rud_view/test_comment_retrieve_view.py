import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.comments_serializers import CommentSerializer
from factories import CommentFactory


class TestCommentRetrieveAPIView:
    @pytest.mark.django_db
    def test_comment_retrieve_view(self, client_and_comment):
        client, comment = client_and_comment

        response = client.get(
            f'/goals/goal_comment/{comment.pk}'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data == CommentSerializer(comment).data, 'Вернулись неверные данные'

    @pytest.mark.django_db
    def test_category_retrieve_view_errors(self, client, users_comment, user_with_password):
        comment = users_comment
        not_user_comment = CommentFactory.create()

        # Обращение неавторизованного пользователя
        response_1 = client.get(
            f'/goals/goal_comment/{comment.pk}'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение к чужому комментарию
        user, password = user_with_password
        client.login(username=user.username, password=password)
        response_2 = client.get(
            f'/goals/goal_comment/{not_user_comment.pk}'
        )
        assert response_2.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к несуществующему комментарию
        response_3 = client.get(
            f'/goals/goal_category/100000000'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'
