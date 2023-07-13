from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers.comments_serializers import CommentSerializer, CommentCreateSerializer
from ..filters import CommentFilter
from ..models import Comment, Goal
from ..permission import CreateCommentPermissions, CommentPermissions


@extend_schema_view(
    post=extend_schema(request=CommentCreateSerializer,
                       description='Create new comment for goal', summary='Create comment',
                       responses={201: OpenApiResponse(response=CommentCreateSerializer,
                                                       description='Comment has been created'),
                                  400: OpenApiResponse(response=CommentCreateSerializer.errors,
                                                       description='Bad Request, (something invalid)'),
                                  403: OpenApiResponse(description="You don't have permission")}))
class CommentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, CreateCommentPermissions]
    serializer_class = CommentCreateSerializer


@extend_schema_view(
    get=extend_schema(description="Goal's comments list", summary='Comments list',
                      responses={200: OpenApiResponse(response=CommentSerializer, description='Comments list'),
                                 403: OpenApiResponse(description="You don't have permission")}))
class CommentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CommentFilter
    ordering_fields = ('created', '-updated')
    ordering = ['-created', '-updated']

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user=self.request.user).exclude(
            goal__status=Goal.StatusChoices.archived).select_related('user')


@extend_schema_view(
    get=extend_schema(request=CommentSerializer,
                      description='Get full information about comment', summary='Comment detail',
                      responses={200: OpenApiResponse(response=CommentSerializer, description='Comment information'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    put=extend_schema(request=CommentSerializer,
                      description='Update comment\'s text', summary='Update comment',
                      responses={200: OpenApiResponse(response=CommentSerializer,
                                                      description='Comment\'s text has been updated'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    delete=extend_schema(request=CommentSerializer,
                         description='Delete comment', summary='Delete comment',
                         responses={
                             204: OpenApiResponse(response={}, description='Comment has been deleted'),
                             403: OpenApiResponse(description="You don't have permission")}))
class CommentRUDAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, CommentPermissions]
    serializer_class = CommentSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Comment.objects.exclude(goal__status=Goal.StatusChoices.archived).select_related('user')
