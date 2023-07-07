import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from goals.serializers.comments_serializers import CommentSerializer
from factories import CommentFactory, GoalFactory


class TestCommentUpdateView:
    @pytest.mark.django_db
    def test_comment_update_view(self, client_and_comment):
        client, comment = client_and_comment
        goal = comment.goal
        category = goal.category

        data = {
            'text': 'new_text',
            'goal': goal.pk,
        }
        response = client.put(
            f'/goals/goal_comment/{comment.pk}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_200_OK, \
            f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
        assert response.data['text'] == data['text'], 'Текст не обновилось'
        assert response.data['updated'] != response.data['created'], 'Время обновления не установилось'
        comment.refresh_from_db()
        assert comment.updated > comment.created, 'Время обновления раньше времени создания'
        assert response.data == CommentSerializer(comment).data, 'Вернулись неверные данные'
        assert comment.goal == goal, 'Обновилась цель'
        assert comment.goal.category == category, 'Обновилась категория'

    @pytest.mark.django_db
    def test_comment_update_view_errors(self, client, users_comment, user_with_password):
        comment = users_comment
        goal = comment.goal
        user, password = user_with_password
        not_users_comment = CommentFactory.create()
        not_user_goal = GoalFactory.create()

        # Обращение неавторизованного пользователя
        data_1 = {
            'text': 'new_title',
            'goal': goal.pk,
        }
        response_1 = client.put(
            f'/goals/goal_comment/{comment.pk}',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение без данных
        client.login(username=user.username, password=password)
        response_2 = client.put(
            f'/goals/goal_comment/{comment.pk}'
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение к чужому комментарию
        data_3 = {
            'text': 'new_text',
            'goal': not_users_comment.goal.pk,
        }
        response_3 = client.put(
            f'/goals/goal_comment/{not_users_comment.pk}',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение к несуществующему комментарию
        data_4 = {
            'text': 'new_text',
            'goal': goal.pk
        }
        response_4 = client.put(
            f'/goals/goal_comment/100000000',
            data=data_4,
            content_type='application/json'
        )
        assert response_4.status_code is HTTP_404_NOT_FOUND, \
            f'Вернулся код {response_4.status_code} вместо {HTTP_404_NOT_FOUND}'

        # Обращение с пустой строкой или None
        data_5 = {
            'text': '',
            'goal': ''
        }
        data_6 = {
            'text': None,
            'goal': None,
        }

        for data in [data_5, data_6]:
            response_5 = client.put(
                f'/goals/goal_comment/{comment.pk}',
                data=data,
                content_type='application/json'
            )
            assert response_5.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_5.status_code} вместо {HTTP_400_BAD_REQUEST}'
            assert {'text', 'goal'} == set(response_5.data.keys()), f'Вернулись не те ошибки'