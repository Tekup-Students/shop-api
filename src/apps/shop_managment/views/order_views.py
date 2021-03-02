# python lib
import datetime
import os
from django.conf import settings

# django lib
from rest_framework import generics, filters, views
from rest_framework.permissions import IsAuthenticated

from ..models.order import Order
from ..serializers.order_serializer import OrderSerializer


class OrderCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    search_fields = (
        'catgory_name',
        'description'
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['catgory_name', 'description']
    ordering = ['pk']


class MyOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AllOrderListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(
        deleted_at__isnull=True,
    )
    pagination_class = None


class OrderUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter(
        deleted_at__isnull=True,
    )


class OrderDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()


class OrderActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
