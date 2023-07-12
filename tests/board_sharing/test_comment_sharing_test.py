import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from goals.serializers.comments_serializers import CommentSerializer
from factories import CategoryFactory, GoalFactory, CommentFactory


class TestCommentSharing:
    SIZE = 5
    PAGE = 300
    ALIEN_INDEX = 0
    READER_INDEX = 1
    OWNER_INDEX = 3

    @pytest.mark.django_db
    def test_comments_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)
        comments = CommentFactory.create_batch(user=owner, goal=goal, size=self.SIZE)
        comments.sort(key=lambda c: c.created, reverse=True)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.get(
                '/goals/goal_comment/list',
                data={'limit': self.PAGE, 'goal': goal.pk}
            )

            assert response.status_code is HTTP_200_OK, \
                f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'

            if i == self.ALIEN_INDEX:
                assert response.data['count'] == 0, 'Есть данные у не участника'

            else:
                assert response.data['count'] == self.SIZE, 'Неверное количество записей для владельца'
                assert response.data['results'] == CommentSerializer(comments, many=True).data, \
                    f'Вернулись неверные данные для владельца'

    @pytest.mark.django_db
    def test_comment_create_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'text': f'new_text_by_{i}',
                'goal': goal.pk
            }
            response = client.post(
                f'/goals/goal_comment/create',
                data=data,
                content_type='application/json'
            )

            if i == self.ALIEN_INDEX:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_201_CREATED, \
                    f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'
                assert response.data['text'] == data['text'], f'Название не установилось {i}'
                goal.refresh_from_db()
                comment = goal.comments.last()
                assert comment.user == user, f'Неверный автор {i}'

    @pytest.mark.django_db
    def test_comment_edit_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)
        comment = CommentFactory.create(user=owner, goal=goal)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'text': f'new_text_by_{i}',
            }
            response = client.put(
                f'/goals/goal_comment/{comment.pk}',
                data=data,
                content_type='application/json'
            )

            if i == self.OWNER_INDEX:
                assert response.status_code is HTTP_200_OK, \
                    f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
                assert response.data['text'] == data['text'], 'Название не обновилось'
                comment.refresh_from_db()
                assert comment.user == owner, 'Обновился автор'

            else:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

    @pytest.mark.django_db
    def test_goal_delete_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)
        comment = CommentFactory.create(user=owner, goal=goal)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.delete(
                f'/goals/goal_comment/{comment.pk}',
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_204_NO_CONTENT, \
                    f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'
                comment = CommentFactory.create(user=owner, goal=goal)
