from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from goals.models import Category, Goal
from goals.permission import CategoryPermissions, CreateCategoryPermissions
from ..filters import CategoryFilter
from ..serializers.categorises_serializers import CategoryCreateSerializer, CategorySerializer
from rest_framework import filters


@extend_schema_view(
    post=extend_schema(request=CategoryCreateSerializer,
                       description='Create new categories for goals', summary='Create category',
                       responses={201: OpenApiResponse(response=CategoryCreateSerializer,
                                                       description='Category has been created'),
                                  400: OpenApiResponse(response=CategoryCreateSerializer.errors,
                                                       description='Bad Request, (something is invalid)'),
                                  403: OpenApiResponse(description="You don't have permission")}))
class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated, CreateCategoryPermissions]


@extend_schema_view(
    get=extend_schema(description="User's categories list", summary='Categories list',
                      responses={200: OpenApiResponse(response=CategorySerializer, description='Categories list'),
                                 403: OpenApiResponse(description="You don't have permission")}))
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_class = CategoryFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        # return Category.objects.filter(user=self.request.user, is_deleted=False).select_related('user')
        return Category.objects.filter(board__participants__user=self.request.user, is_deleted=False).select_related(
            'user')



@extend_schema_view(
    get=extend_schema(request=CategorySerializer,
                      description='Get full information about category', summary='Category detail',
                      responses={200: OpenApiResponse(response=CategorySerializer, description='Category information'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    put=extend_schema(request=CategorySerializer,
                      description='Update category information', summary='Update category',
                      responses={200: OpenApiResponse(response=CategorySerializer,
                                                      description='Board has been updated'),
                                 403: OpenApiResponse(description="You don't have permission")}),
    delete=extend_schema(request=CategorySerializer,
                         description='Delete category and category\'s goals', summary='Delete category',
                         responses={
                             204: OpenApiResponse(response={}, description='Category has been deleted'),
                             403: OpenApiResponse(description="You don't have permission")}),
)
class CategoryRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermissions]
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False).select_related('user')

    def perform_destroy(self, instance: Category) -> Category:
        instance.goals.update(status=Goal.StatusChoices.archived)
        instance.is_deleted = True
        instance.save()
        return instance
