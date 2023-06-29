import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST


class TestUsersPasswordUpdateView:
    @pytest.mark.django_db
    def test_users_password_update_view(self, client, user_with_password):
        user, password = user_with_password
        client.login(username=user.username, password=password)
        data = {
            'old_password': password,
            'new_password': password + '1',
        }

        response = client.put(
            '/core/update_password',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == HTTP_200_OK, \
            f'Возвращается код {response.status_code} вместо {HTTP_200_OK}'
        user.refresh_from_db()

        assert not user.check_password(password), 'Пароль пользователя не изменился'
        assert user.password != data['new_password'], 'Новый пароль не в хешированном виде'
        assert user.check_password(data['new_password']), 'Новый пароль установлен неправильно'

    @pytest.mark.django_db
    def test_users_password_update_view_errors(self, client, user_with_password, simple_password):
        user, password = user_with_password

        # Обращение без токена
        data_1 = {
            'old_password': password,
            'new_password': password + '1',
        }

        response_1 = client.put(
            '/core/update_password',
            data=data_1,
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_403_FORBIDDEN, \
            f'Возвращается код {response_1.status_code} вместо {HTTP_403_FORBIDDEN}'

        # Обращение без данных
        client.login(username=user.username, password=password)
        response_2 = client.put(
            '/core/update_password'
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается статус {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с неверным паролем
        data_3 = {
            'old_password': 'wrong_password',
            'new_password': password + '1'
        }
        response_3 = client.put(
            '/core/update_password',
            data=data_3,
            content_type='application/json'
        )
        assert response_3.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается статус {response_3.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с простым новым паролем
        data_4 = {
            'old_password': password,
            'new_password': simple_password,
        }
        response_4 = client.put(
            '/core/update_password',
            data=data_4,
            content_type='application/json',
        )
        assert response_4.status_code == HTTP_400_BAD_REQUEST, \
            f'Возвращается статус {response_4.status_code} вместо {HTTP_400_BAD_REQUEST}'
        user.refresh_from_db()
        assert user.check_password(password), 'Обновился пароль у пользователя'
