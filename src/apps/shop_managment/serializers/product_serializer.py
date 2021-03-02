import datetime
from rest_framework import serializers
from ..models.product import Product, ProductImage, Category
from .category_serializer import CategorySerializer

from core.mixins.serializers import UniqueFieldsMixin, CustomRelatedField

class ProductImageSerializer(UniqueFieldsMixin):
    class Meta:
        model = ProductImage
        fields = (
            'id',
            'image',
        )
        read_only_fields = (
            'id',
        )

class ProductSerializer(UniqueFieldsMixin):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CustomRelatedField(serializer_class=CategorySerializer, model=Category)
    product_image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'images',
            'product_image',
            'product_name',
            'description',
            'price',
            'stock',
            'category',
            'created_at',
            'is_active',
        )
        read_only_fields = (
            'id',
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
