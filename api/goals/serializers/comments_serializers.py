from rest_framework import serializers
from ..models import Comment, StatusChoices
from core.serializers import UserSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('user', 'text', 'goal')

    def validate_goal(self, goal):
        if goal.status is StatusChoices.archived:
            raise serializers.ValidationError('not allowed in deleted goal')
        if goal.user is not self.context['request'].user:
            raise serializers.ValidationError('not owner of goal')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created', 'updated')
