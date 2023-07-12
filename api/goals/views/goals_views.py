from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from ..serializers.goals_serializers import GoalCreateSerializer, GoalSerializer
from ..models import Goal
from ..filters import GoalFilter
from ..permission import GoalPermissions, CreateGoalPermissions


class GoalCreateAPIView(CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated, CreateGoalPermissions]


class GoalListAPIView(ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalFilter
    ordering_fields = ['-priority', 'due_date']
    ordering = ['-priority', 'due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user).exclude(
            status=Goal.StatusChoices.archived).select_related('user')


class GoalRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        return Goal.objects.exclude(status=Goal.StatusChoices.archived).select_related('user')

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.StatusChoices.archived
        instance.save()
        return instance
