from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from ..serializers.board_serializer import BoardCreateSerializer, BoardListSerializer, BoardSerializer
from ..models import Board, Goal
from ..permission import BoardPermissions


@extend_schema_view(
    post=extend_schema(request=BoardCreateSerializer,
                       description='Create new board for categories', summary='Create board',
                       responses={201: OpenApiResponse(response=BoardCreateSerializer,
                                                       description='Board has been created'),
                                  400: OpenApiResponse(response=BoardCreateSerializer.errors,
                                                       description='Bad Request, (something invalid)'),
                                  403: OpenApiResponse(description="You don't have permission")}))
class BoardCreateAPIView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    get=extend_schema(description="User's board list", summary='Board list',
                      responses={200: OpenApiResponse(response=BoardListSerializer, description='Board list'),
                                 403: OpenApiResponse(description="You don't have permission")}))
class BoardListAPIView(generics.ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title']
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


@extend_schema_view(
    get=extend_schema(request=BoardSerializer,
                      description='Get full information about board', summary='Board detail',
                      responses={200: OpenApiResponse(response=BoardSerializer, description='Board information'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    put=extend_schema(request=BoardSerializer,
                      description='Update information or participants in board', summary='Update board',
                      responses={200: OpenApiResponse(response=BoardSerializer, description='Board has been updated'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    delete=extend_schema(request=BoardSerializer,
                         description='Delete board and board\'s categories and goals', summary='Delete board',
                         responses={
                             204: OpenApiResponse(response={}, description='Board has been deleted'),
                             403: OpenApiResponse(description="You don't have permission")}))
class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, BoardPermissions]
    http_method_names = ['get', 'put', 'delete']

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
