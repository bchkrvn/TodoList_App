from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from goals.models import Category, Goal, StatusChoices
from goals.permission import IsOwner
from ..serializers.categorises_serializers import CategoryCreateSerializer, CategorySerializer, \
    CategorySerializerRUD
from rest_framework import filters


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated]


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_deleted=False).select_related('user')


class CategoryRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerRUD
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_deleted=False).select_related('user')

    def perform_destroy(self, instance: Category):
        instance.goals.update(status=StatusChoices.archived)
        instance.is_deleted = True
        instance.save()
        return instance
