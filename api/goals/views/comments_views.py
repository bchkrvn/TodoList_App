from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers.comments_serializers import CommentSerializer, CommentCreateSerializer
from ..filters import CommentFilter
from ..models import Comment, StatusChoices
from ..permission import IsOwner


class CommentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CommentFilter
    ordering_fields = ('created', '-updated')
    ordering = ['-created', '-updated']

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).exclude(
            goal__status=StatusChoices.archived).select_related('user')


class CommentRUDAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).exclude(
            goal__status=StatusChoices.archived).select_related('user')
