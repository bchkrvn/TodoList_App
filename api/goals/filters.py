from django.db import models
from django_filters import rest_framework, IsoDateTimeFilter

from .models import Goal, Comment


class GoalFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ('gte', 'lte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }

        filter_overrides = {
            models.DateTimeField: {"filter_class": IsoDateTimeFilter},
        }


class CommentFilter(rest_framework.FilterSet):
    class Meta:
        model = Comment
        fields = ['goal']
