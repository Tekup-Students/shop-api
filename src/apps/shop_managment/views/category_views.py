# python lib
import datetime
import os
from django.conf import settings

# django lib
from rest_framework import generics, filters, views
from rest_framework.permissions import IsAuthenticated

from ..models.category import Category
from ..serializers.category_serializer import CategorySerializer


class CategoryCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    search_fields = (
        'catgory_name',
        'description'
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['catgory_name', 'description']
    ordering = ['pk']


class AllCategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(
        deleted_at__isnull=True,
    )
    pagination_class = None


class CategoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.filter(
        deleted_at__isnull=True,
    )


class CategoryDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()


class CategoryActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
