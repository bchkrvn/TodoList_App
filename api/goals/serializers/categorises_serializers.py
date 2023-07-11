from rest_framework import serializers

from goals.models import Category
from core.serializers import UserSerializer


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'user', 'id', 'created', 'updated', 'board')
        read_only_fields = ('id', 'created', 'updated')


class CategoryCreateSerializer(BaseCategorySerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class CategorySerializer(BaseCategorySerializer):
    user = UserSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)
