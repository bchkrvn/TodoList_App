import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


class TestUsersProfileViewGet:
    @pytest.mark.django_db
    def test_users_profile_view_get(self, client, user_with_password):
        user, password = user_with_password
        client.login(username=user.username, password=password)

        response = client.get(
            '/core/profile'
        )

        assert response.status_code == HTTP_200_OK, \
            f'Возвращается код {response.status_code} вместо {HTTP_200_OK}'

        answer_keys = {'id', "username", 'first_name', 'last_name', 'email'}
        assert answer_keys == set(response.data.keys()), f'Ключи не совпадают'

        assert user.pk == response.data['id'], f'id пользователя не совпадает'
        assert user.username == response.data['username'], f'username пользователя не совпадает'
        assert user.first_name == response.data['first_name'], f'first_name пользователя не совпадает'
        assert user.last_name == response.data['last_name'], f'last_name пользователя не совпадает'
        assert user.email == response.data['email'], f'email пользователя не совпадает'

    @pytest.mark.django_db
    def test_users_profile_view_get_error(self, client):
        # Обращение без токена
        response = client.get(
            '/core/profile'
        )

        assert response.status_code == HTTP_403_FORBIDDEN, \
            f'Возвращается код {response.status_code} вместо {HTTP_403_FORBIDDEN}'
