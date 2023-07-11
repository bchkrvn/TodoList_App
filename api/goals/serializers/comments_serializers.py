from rest_framework import serializers
from ..models import Comment, Goal
from core.serializers import UserSerializer


class BaseCommentSerializer(serializers.ModelSerializer):

    def validate_goal(self, goal):
        if goal.status == Goal.StatusChoices.archived:
            raise serializers.ValidationError('not allowed in deleted goal')
        return goal

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class CommentCreateSerializer(BaseCommentSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class CommentSerializer(BaseCommentSerializer):
    user = UserSerializer(read_only=True)
