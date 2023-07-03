from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from ..serializers.goals_serializers import GoalCreateSerializer, GoalSerializer
from ..permission import IsOwner
from ..models import Goal, StatusChoices
from ..goals_filters import GoalFilter


class GoalCreateAPIView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalListAPIView(ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalFilter
    ordering_fields = ['-priority', 'due_date']
    ordering = ['-priority', 'due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).exclude(status=4).select_related('user').select_related(
            'category')


class GoalRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).exclude(status=4).select_related('user').select_related(
            'category')

    def perform_destroy(self, instance: Goal):
        instance.status = StatusChoices.archived
        instance.save()
        return instance
