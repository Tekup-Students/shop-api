import datetime
from rest_framework import serializers
from ..models.category import Category
from core.mixins.serializers import UniqueFieldsMixin


class CategorySerializer(UniqueFieldsMixin):
    class Meta:
        model = Category
        fields = (
            'id',
            'category_name',
            'description',
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
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(validated_data)
        return super().update(instance, validated_data)
