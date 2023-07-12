import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Comment
from factories import GoalFactory


class TestCommentCreateView:
    @pytest.mark.django_db
    def test_comment_create_view(self, login_client_with_user, client_and_goal):
        client, goal = client_and_goal
        data = {
            'text': 'Test text',
            'goal': goal.pk,
        }
        response = client.post(
            '/goals/goal_comment/create',
            data=data,
            content_type='application/json'
        )
        assert response.status_code is HTTP_201_CREATED, \
            f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'

        new_comment = Comment.objects.last()
        assert new_comment.text == data['text'], 'Неверное название у комментария'
        assert new_comment.goal == goal, 'Неверная цель у комментария'
        assert new_comment.user == goal.user, 'Неверный автор у комментария'
        assert new_comment.created is not None, 'Нет даты создания'
        assert new_comment.updated is not None, 'Нет даты обновления'

    @pytest.mark.django_db
    def test_comment_create_view_errors(self, client, client_and_goal):
        client, goal = client_and_goal
        not_users_goal = GoalFactory.create()

        # Обращение без данных
        response_2 = client.post(
            '/goals/goal_comment/create',
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с пустой строкой
        data_3 = {
            'text': '',
            "goal": goal.pk,
        }
        response_3_1 = client.post(
            '/goals/goal_comment/create',
            data=data_3,
            content_type='application/json'
        )
        assert response_3_1.status_code == HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_3_1.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с чужой или несуществующей целью
        data_3_1 = {
            'text': 'some text',
            "goal": not_users_goal.pk,
        }
        data_3_2 = {
            'text': 'some text',
            "goal": 100000000000,
        }

        response_3_1 = client.post(
            '/goals/goal_comment/create',
            data=data_3_1,
            content_type='application/json'
        )
        assert response_3_1.status_code == HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        response_3_2 = client.post(
            '/goals/goal_comment/create',
            data=data_3_2,
            content_type='application/json'
        )
        assert response_3_2.status_code == HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_3_2.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение без авторизации
        client.logout()
        data_1 = {
            'text': 'Test title',
            'goal': goal.pk,
        }
        response_1 = client.post(
            '/goals/goal_comment/create',
            data=data_1,
            content_type='application/json'
        )
        assert response_1.status_code is HTTP_403_FORBIDDEN, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'
