import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from goals.serializers.goals_serializers import GoalSerializer
from factories import CategoryFactory, GoalFactory


class TestGoalSharing:
    SIZE = 5
    PAGE = 300
    ALIEN_INDEX = 0
    READER_INDEX = 1

    @pytest.mark.django_db
    def test_goals_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goals = GoalFactory.create_batch(user=owner, category=category, size=self.SIZE)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.get(
                '/goals/goal/list',
                data={'limit': self.PAGE}
            )

            assert response.status_code is HTTP_200_OK, \
                f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'

            if i == self.ALIEN_INDEX:
                assert response.data['count'] == 0, 'Есть данные у не участника'

            else:
                assert response.data['count'] == self.SIZE, 'Неверное количество записей для владельца'
                assert response.data['results'] == GoalSerializer(goals, many=True).data, \
                    f'Вернулись неверные данные для владельца'

    @pytest.mark.django_db
    def test_goal_create_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'title': f'new_title_by_{i}',
                'category': category.pk
            }
            response = client.post(
                f'/goals/goal/create',
                data=data,
                content_type='application/json'
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_201_CREATED, \
                    f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'
                assert response.data['title'] == data['title'], 'Название не установилось'
                category.refresh_from_db()
                goal = category.goals.last()
                assert goal.user == user, 'Неверный автор цели'

    @pytest.mark.django_db
    def test_goal_edit_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'title': f'new_title_by_{i}',
                'category': category.pk,
            }
            response = client.put(
                f'/goals/goal/{goal.pk}',
                data=data,
                content_type='application/json'
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_200_OK, \
                    f'Вернулся код {response.status_code} вместо {HTTP_200_OK}'
                assert response.data['title'] == data['title'], 'Название не обновилось'
                goal.refresh_from_db()
                assert goal.user == owner, 'Обновился автор цели'

    @pytest.mark.django_db
    def test_goal_delete_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)
        goal = GoalFactory.create(user=owner, category=category)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.delete(
                f'/goals/goal/{goal.pk}',
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_204_NO_CONTENT, \
                    f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'
                goal = GoalFactory.create(user=owner, category=category)
