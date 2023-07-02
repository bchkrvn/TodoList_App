from rest_framework import serializers

from goals.models import Category
from core.serializers import UserSerializer


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('title', 'user', 'id', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Category
        fields = ('title', 'user', 'id', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated', 'user')


class CategorySerializerRUD(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'id', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')
