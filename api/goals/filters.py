from django_filters import rest_framework

from .models import Goal, Comment, Category


class GoalFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ('gte', 'lte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }


class CommentFilter(rest_framework.FilterSet):
    class Meta:
        model = Comment
        fields = ['goal']


class CategoryFilter(rest_framework.FilterSet):
    class Meta:
        model = Category
        fields = ['board']
