import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class TestUserLoginView:
    @pytest.mark.django_db
    def test_user_login_view(self, client, user_with_password):
        user, password = user_with_password
        data = {
            'username': user.username,
            'password': password,
        }

        response = client.post(
            '/core/login',
            data=data,
            content_type='application/json',
        )

        assert response.status_code == HTTP_200_OK, f'Возвращается код {response.status_code} вместо {HTTP_200_OK}'

        answer_keys = {'id', 'username', 'first_name', 'last_name', 'email'}
        assert answer_keys == set(response.data.keys()), 'Возвращаются не те ключи'

        assert 'sessionid' in response.cookies.keys(), 'В cookies нет sessionid'
        assert response.cookies['sessionid'] is not None, 'Нет токена sessionid'

    @pytest.mark.django_db
    def test_user_login_view_errors(self, client, user_with_password):
        user, password = user_with_password

        # Обращение без данных
        response_1 = client.post(
            '/core/login',
        )

        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается код {response_1.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert 'sessionid' not in response_1.cookies.keys(), 'В cookies есть sessionid'

        # Несуществующий пользователь
        data_2 = {
            'username': 'wrong_user_name',
            'password': 'wrong_password',
        }
        response_2 = client.post(
            '/core/login',
            data=data_2,
            content_type='application/json'
        )

        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert 'sessionid' not in response_2.cookies.keys(), 'В cookies есть sessionid'

        # Неверный пароль
        data_3 = {
            'username': user.username,
            'password': 'wrong_password',
        }

        response_3 = client.post(
            '/core/login',
            data=data_3,
            content_type='application/json',
        )

        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается код {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'
        assert 'sessionid' not in response_3.cookies.keys(), 'В cookies есть sessionid'
