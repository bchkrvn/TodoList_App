from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSingUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='Имя пользователя уже занято')])
    password_repeat = serializers.CharField(max_length=128,
                                            style={'input_type': 'password'},
                                            write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message='Адрес электронной почты уже используется')])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password_repeat(self, password_repeat):
        cd = self.initial_data
        if cd['password'] != cd['password_repeat']:
            raise serializers.ValidationError("Пароли не совпадают")
        return password_repeat

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return password

    def create(self, validated_data):
        del validated_data['password_repeat']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='Имя пользователя уже занято')])

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message='Адрес электронной почты уже используется')])

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate_new_password(self, new_password):
        try:
            validate_password(new_password)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return new_password

    def validate_old_password(self, old_password):
        if self.context['request'].user.check_password(old_password):
            return old_password
        else:
            raise serializers.ValidationError('Старый пароль введен неверно')

    def save(self, **kwargs):
        user = self.instance
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
