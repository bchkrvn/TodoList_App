import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from core.models import User


class TestUserSingUpView:
    @pytest.mark.django_db
    def test_users_sing_up_view(self, password, client):
        data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'Test@test.test',
            'username': 'test',
            'password': password,
            'password_repeat': password,
        }

        response = client.post(
            '/core/signup',
            data=data,
            content_type='application/json',
        )
        assert response.status_code == HTTP_201_CREATED, \
            f'Вернулся код {response.status_code} вместо {HTTP_201_CREATED}'

        answer_key = {'first_name', 'last_name', 'email', 'username'}

        assert answer_key == set(response.data.keys()), 'Вернулись не те ключи'
        user = User.objects.last()

        assert user.first_name == data['first_name'], 'Неверно first_name пользователя'
        assert user.last_name == data['last_name'], 'Неверно last_name пользователя'
        assert user.email == data['email'], 'Неверно email пользователя'
        assert user.username == data['username'], 'Неверно username пользователя'
        assert user.password != data['password'], 'Пароль не захеширован'
        assert user.check_password(data['password']), 'Установлен неверный пароль'

    @pytest.mark.django_db
    def test_users_sing_up_errors(self, user, password, client, simple_password):
        # Обращение без данных
        response_1 = client.post(
            '/core/signup',
            content_type='application/json',
        )
        assert response_1.status_code == HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_1.status_code} вместо {HTTP_400_BAD_REQUEST}'

        # Обращение с повторяющимся username, легким паролем и неверный повторным паролем
        data_2 = {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'Test@test.test',
            'username': user.username,
            'password': simple_password,
            'password_repeat': password,
        }

        response_2 = client.post(
            '/core/signup',
            data=data_2,
            content_type='application/json',
        )
        assert response_2.status_code == HTTP_400_BAD_REQUEST, \
            f'Вернулся код {response_2.status_code} вместо {HTTP_400_BAD_REQUEST}'

        assert 'username' in response_2.data, 'Нет сообщения об ошибке username'
        assert 'password' in response_2.data, 'Нет сообщения об ошибке password'
        assert 'password_repeat' in response_2.data, 'Нет сообщения об ошибке password_repeat'
