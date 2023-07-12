import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND

from goals.serializers.categorises_serializers import CategorySerializer

from factories import CategoryFactory


class TestCategorySharing:
    SIZE = 5
    PAGE = 10
    ALIEN_INDEX = 0
    READER_INDEX = 1
    WRITER_INDEX = 2
    OWNER_INDEX = 3

    @pytest.mark.django_db
    def test_categories_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        categories = CategoryFactory.create_batch(user=owner, board=board, size=self.SIZE)
        categories.sort(key=lambda c: c.title)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.get(
                '/goals/goal_category/list',
                data={'limit': self.PAGE}
            )

            assert response.status_code is HTTP_200_OK, \
                f'Вернулся код  {response.status_code} вместо {HTTP_200_OK}'

            if i == self.ALIEN_INDEX:
                assert response.data['count'] == 0, 'Есть данные у не участника'

            else:
                assert response.data['count'] == self.SIZE, 'Неверное количество записей для владельца'
                assert response.data['results'] == CategorySerializer(categories, many=True).data, \
                    f'Вернулись неверные данные для владельца'

    @pytest.mark.django_db
    def test_category_create_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'title': f'new_title_by_{i}',
                'board': board.pk,
            }
            response = client.post(
                f'/goals/goal_category/create',
                data=data,
                content_type='application/json'
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_201_CREATED, \
                    f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'
                assert response.data['title'] == data['title'], 'Название не обновилось'
                board.refresh_from_db()
                category = board.categories.last()
                assert category.user == user, 'Обновился автор категории'

    @pytest.mark.django_db
    def test_category_edit_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            data = {
                'title': f'new_title_by_{i}'
            }
            response = client.put(
                f'/goals/goal_category/{category.pk}',
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
                category.refresh_from_db()
                assert category.user == owner, 'Обновился автор категории'

    @pytest.mark.django_db
    def test_category_delete_sharing(self, client, one_board_owner_writer_reader_alien):
        board, owner, writer, reader, alien = one_board_owner_writer_reader_alien
        category = CategoryFactory.create(user=owner, board=board)

        for i, user in enumerate([alien, reader, writer, owner]):
            client.force_login(user)
            response = client.delete(
                f'/goals/goal_category/{category.pk}',
            )

            if i in [self.READER_INDEX, self.ALIEN_INDEX]:
                assert response.status_code is HTTP_403_FORBIDDEN, \
                    f'Вернулся код  {response.status_code} вместо {HTTP_403_FORBIDDEN}'

            else:
                assert response.status_code is HTTP_204_NO_CONTENT, \
                    f'Вернулся код {response.status_code} вместо {HTTP_204_NO_CONTENT}'
                category = CategoryFactory.create(user=owner, board=board)
