from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from ..serializers.goals_serializers import GoalCreateSerializer, GoalSerializer
from ..permission import IsOwner
from ..models import Goal, StatusChoices
from ..filters import GoalFilter


class GoalCreateAPIView(CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalListAPIView(ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalFilter
    ordering_fields = ['-priority', 'due_date']
    ordering = ['-priority', 'due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=StatusChoices.archived).select_related('user')


class GoalRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=StatusChoices.archived).select_related('user')

    def perform_destroy(self, instance: Goal):
        instance.status = StatusChoices.archived
        instance.save()
        return instance