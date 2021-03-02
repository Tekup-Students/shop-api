from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers

from ..models import Profile
from ..exceptions import WrongPasswordException
from .group_serializer import PermissionSerializer, GroupSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    display_permissions = serializers.SerializerMethodField()
    display_groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_superuser',
            'user_permissions',
            'display_permissions',
            'groups',
            'display_groups'
        )
        extra_kwargs = {
            'user_permissions': {'required': False},
            'groups': {'required': False},
        }
        read_only_fields = (
            'id',
            'display_permissions',
            'display_groups',
            'is_active'
        )

    def to_internal_value(self, data):
        permission_data = data.get('user_permissions', None)
        if not permission_data:
            data['user_permissions'] = []
        return data

    def get_display_permissions(self, obj):
        return PermissionSerializer(obj.user_permissions, many=True).data
    
    def get_user_permissions(self, obj):
        return obj.user_permissions.all().values_list('codename', flat=True)

    def get_display_groups(self, obj):
        return GroupSerializer(obj.groups, many=True).data


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )
        read_only_fields = (
            'id',
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'id',
            'address',
            'phone',
            'user',
            'is_active',
        )
        extra_kwargs = {
            'user': {'required': True},
        }
        read_only_fields = (
            'id',
            'is_active',
        )

    def create(self, validated_data):
        current_user = self.context.get('request').user
        created_by = current_user

        user_data = validated_data.pop('user')
        permission_data = user_data.pop('user_permissions', None)
        groups_data = user_data.pop('groups', None)

        user = User(**user_data, is_active=True)
        user.save()

        if permission_data:
            permissions = Permission.objects.filter(codename__in=permission_data).all()
            user.user_permissions.set(permissions)

        if groups_data:
            user.set_groups(groups_data)
        
        profile = Profile.objects.create(
            user=user,
            created_by=created_by,
            **validated_data
        )
        
        return profile

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        updated_by = current_user

        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)

        user_data = validated_data.pop('user', None)
        user = instance.user
        if user_data:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)

        permission_data = user_data.get('user_permissions', instance.user.user_permissions)
        if permission_data:
            user.user_permissions.set(Permission.objects.filter(codename__in=permission_data).all())

        groups_data = user_data.get('groups', instance.user.groups)
        if groups_data:
            user.groups.set(groups_data)

        instance.save()
        user.save()

        return instance


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'id',
            'is_superuser'
        )
        read_only_fields = (
            'id',
        )


class CurrentProfileSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer()
    current_password = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = (
            'phone',
            'address',
            'user',
            'current_password'
        )
        extra_kwargs = {
            'user': {'required': True}, 'current_password': { 'write_only': True }
        }

    def validate(self, attrs):
        current_user = self.context.get('request').user
        current_password = attrs.get('current_password')

        if not current_user.check_password(current_password):
            raise WrongPasswordException('Wrong password.')

        return super().validate(attrs)

    def update(self, instance, validated_data):
        current_user = self.context.get('request').user
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        
        user_data = validated_data.pop('user', None)
        user = instance.user
        if user_data:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.username = user_data.get('username', user.username)
            new_email = user_data.get('email', user.email)

        instance.save()
        user.save()

        return instance


class UpdateCurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)

    def validate(self, data):
        current_user = self.context.get('request').user
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_user.check_password(current_password):
            raise WrongPasswordException('Wrong password.')
        current_user.set_password(new_password)
        current_user.save()

        return data
