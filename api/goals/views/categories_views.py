from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from goals.models import Category, Goal
from goals.permission import CategoryPermissions, CreateCategoryPermissions
from ..filters import CategoryFilter
from ..serializers.categorises_serializers import CategoryCreateSerializer, CategorySerializer
from rest_framework import filters


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated, CreateCategoryPermissions]


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
        return Category.objects.filter(board__participants__user=self.request.user, is_deleted=False).select_related('user')


class CategoryRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermissions]

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False).select_related('user')

    def perform_destroy(self, instance: Category):
        instance.goals.update(status=Goal.StatusChoices.archived)
        instance.is_deleted = True
        instance.save()
        return instance
