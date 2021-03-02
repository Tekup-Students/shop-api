import datetime
from rest_framework import serializers
from core.mixins.serializers import NestedCreateMixin, CustomRelatedField, UniqueFieldsMixin, NestedUpdateMixin
from ..models.order import Order, OrderItem
from .product_serializer import ProductSerializer, Product


class OrderItemSerializer(UniqueFieldsMixin):
    product = CustomRelatedField(serializer_class=ProductSerializer, model=Product)
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'price',
            'cost',
            'quantity',
            'created_at',
            'is_active',
        )
        read_only_fields = (
            'id',
            'price',
            'cost',
            'created_at',
            'is_active',
        )


class OrderSerializer(NestedUpdateMixin, NestedCreateMixin):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'address',
            'status',
            'items',
            'total_cost',
            'user',
            'created_at',
            'is_active',
        )
        read_only_fields = (
            'id',
            'total_cost',
            'created_at',
            'is_active',
        )

    def create(self, validated_data):
        current_user = self.context.get('request').user
        validated_data['created_by'] = current_user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        validated_data['updated_by'] = current_user
        validated_data['updated_at'] = datetime.datetime.now()
        return super().update(instance, validated_data)
