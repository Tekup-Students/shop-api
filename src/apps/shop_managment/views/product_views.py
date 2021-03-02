# python lib
import datetime
import os
from django.conf import settings

# django lib
from rest_framework import generics, filters, views
from rest_framework.permissions import IsAuthenticated

from ..models.product import Product
from ..serializers.product_serializer import ProductSerializer


class ProductCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    #permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    search_fields = (
        'catgory_name',
        'description'
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['catgory_name', 'description']
    ordering = ['pk']


class AllProductListAPIView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(
        deleted_at__isnull=True,
    )
    pagination_class = None


class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.filter(
        deleted_at__isnull=True,
    )


class ProductDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()


class ProductActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
