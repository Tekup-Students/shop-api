from rest_framework import serializers
from django.contrib.auth.models import Permission, Group


class PermissionSerializer(serializers.ModelSerializer):
    app = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'app',
            'model',
            'codename',
        )

    def get_app(self, obj):
        return obj.content_type.app_label

    def get_model(self, obj):
        return obj.content_type.model


class GroupSerializer(serializers.ModelSerializer):
    display_permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
            'display_permissions',
        )
        extra_kwargs = {'permissions': {'write_only': True}}
        read_only_fields = (
            'id',
        )

    def get_display_permissions(self, obj):
        return PermissionSerializer(obj.permissions, many=True).data

