from rest_framework import serializers
from ..models import Goal
from core.serializers import UserSerializer


class BaseGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['created', 'updated']

    def validate_category(self, category):
        if category.is_deleted:
            raise serializers.ValidationError('This category is deleted')
        return category


class GoalCreateSerializer(BaseGoalSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GoalSerializer(BaseGoalSerializer):
    user = UserSerializer(read_only=True)
