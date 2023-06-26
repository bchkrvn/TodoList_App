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

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate_password_repeat(self, password_repeat):
        cd = self.initial_data
        if cd['password'] != cd['password_repeat']:
            raise serializers.ValidationError("Пароли не совпадают")
        return cd['password_repeat']

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


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    # def validate_password(self, password):
    #     if self.context['request'].user.check_password(password):
    #         return password
    #     else:
    #         raise serializers.ValidationError('Неверный пароль')
