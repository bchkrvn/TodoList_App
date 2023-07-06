import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Comment
from factories import GoalFactory


class TestCommentCreateView:
    @pytest.mark.django_db
    def test_comment_create_view(self, login_client_with_user):
        client, user = login_client_with_user
        goal = GoalFactory.create(user=user)
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
        assert new_comment.user == user, 'Неверный автор у комментария'
        assert new_comment.created is not None, 'Нет даты создания'
        assert new_comment.updated is not None, 'Нет даты обновления'

    @pytest.mark.django_db
    def test_comment_create_view_errors(self, client, user_with_password):
        user, password = user_with_password
        goal = GoalFactory.create(user=user)
        not_users_goal = GoalFactory.create()

        # Обращение без авторизации
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

        # Обращение без данных
        client.login(username=user.username, password=password)
        response_2 = client.post(
            '/goals/goal_comment/create',
        )
        assert response_2.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с пустой строкой
        data_3 = {
            'text': '',
            "goal": goal.pk,
        }
        response_3 = client.post(
            '/goals/goal_comment/create',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code is HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert 'text' in response_3.data, 'Нет сообщения об ошибке text'

        # Обращение с чужой или несуществующей целью
        data_3_1 = {
            'text': 'some text',
            "goal": not_users_goal.pk,
        }
        data_3_2 = {
            'text': 'some text',
            "goal": 100000000000,
        }

        for data in (data_3_1, data_3_2):
            response_3 = client.post(
                '/goals/goal_comment/create',
                data=data,
                content_type='application/json'
            )
            assert response_3.status_code is HTTP_400_BAD_REQUEST, \
                f'Вернулся код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'
            assert 'goal' in response_3.data, 'Нет сообщения об ошибке goal'
