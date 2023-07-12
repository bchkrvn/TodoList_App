from django.db import transaction
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from ..serializers.board_serializer import BoardCreateSerializer, BoardListSerializer, BoardSerializer
from ..models import Board, Goal
from ..permission import BoardPermissions


class BoardCreateAPIView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


class BoardListAPIView(generics.ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title']
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, BoardPermissions]

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False).prefetch_related(
            'participants')

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.StatusChoices.archived)

        return instance
