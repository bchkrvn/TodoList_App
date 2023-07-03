from rest_framework import serializers
from ..models import Goal, Category
from core.serializers import UserSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['created', 'updated']


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def validated_category(self, category):
        if category.user is not self.context['request'].user:
            raise serializers.ValidationError("It isn't your category")
        if category.is_deleted:
            raise serializers.ValidationError('This category is deleted')
        return category

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['created', 'updated']
