from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from ..serializers.goals_serializers import GoalCreateSerializer, GoalSerializer
from ..models import Goal
from ..filters import GoalFilter
from ..permission import GoalPermissions, CreateGoalPermissions


@extend_schema_view(
    post=extend_schema(request=GoalCreateSerializer,
                       description='Create new goal', summary='Create goal',
                       responses={201: OpenApiResponse(response=GoalCreateSerializer,
                                                       description='Goal has been created'),
                                  400: OpenApiResponse(response=GoalCreateSerializer.errors,
                                                       description='Bad Request, (something invalid)'),
                                  403: OpenApiResponse(description="You don't have permission")}))
class GoalCreateAPIView(CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated, CreateGoalPermissions]


@extend_schema_view(
    get=extend_schema(description="User's goals list", summary='Goals list',
                      responses={200: OpenApiResponse(response=GoalSerializer, description='Goals list'),
                                 403: OpenApiResponse(description="You don't have permission")}))
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


@extend_schema_view(
    get=extend_schema(request=GoalSerializer,
                      description='Get full information about goal', summary='Goal detail',
                      responses={200: OpenApiResponse(response=GoalSerializer, description='Goal information'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    put=extend_schema(request=GoalSerializer,
                      description='Update goal information', summary='Update goal',
                      responses={200: OpenApiResponse(response=GoalSerializer, description='Goal has been updated'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    delete=extend_schema(request=GoalSerializer,
                         description='Delete goal and goal\'s comments', summary='Delete goal',
                         responses={204: OpenApiResponse(response={}, description='Goal has been deleted'),
                                    403: OpenApiResponse(description="You don't have permission")}))
class GoalRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, GoalPermissions]
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Goal.objects.exclude(status=Goal.StatusChoices.archived).select_related('user')

    def perform_destroy(self, instance: Goal) -> Goal:
        instance.status = Goal.StatusChoices.archived
        instance.save()
        return instance
