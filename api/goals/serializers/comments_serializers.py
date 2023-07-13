from rest_framework import serializers
from ..models import Comment, Goal
from core.serializers import UserSerializer


class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created', 'updated')

    def validate_goal(self, goal: Goal) -> Goal:
        if goal.status == Goal.StatusChoices.archived:
            raise serializers.ValidationError('Not allowed in deleted goal')
        return goal


class CommentCreateSerializer(BaseCommentSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class CommentSerializer(BaseCommentSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
