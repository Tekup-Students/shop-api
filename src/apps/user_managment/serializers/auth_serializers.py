from django.contrib.auth.models import Permission
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from ..models.profile import Profile
from datetime import datetime
from core.mixins.serializers import NestedCreateMixin, UniqueFieldsMixin, NestedUpdateMixin
from .profile_serializer import PermissionSerializer, ProfileSerializer

#from .send_mail import send_mail_on_frogot_password, send_mail_on_password_reset

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password'
        )
        read_only_fields = (
            'id',
        )


class RegisterSerializer(NestedCreateMixin, UniqueFieldsMixin, NestedUpdateMixin):
    user = RegisterUserSerializer()
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        refresh = RefreshToken().for_user(obj.user)
        return dict(access=str(refresh.access_token))

    class Meta:
        model = Profile
        fields = (
            'id',
            'address',
            'phone',
            'token',
            'user'
        )
        extra_kwargs = {
            'user': {'required': True},
        }
        read_only_fields = (
            'id',
            'token'
        )


class UserLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=self.user)
            data.update(
                profile=ProfileSerializer(profile).data,
                permissions=PermissionSerializer(self.user.user_permissions.all(), many=True).data
            )
        return data


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class ResetPasswordSerializer(serializers.Serializer):
    password = PasswordField(max_length=100)
    token = PasswordField(max_length=32)

    def validate(self, data):
        new_password = data.get('password')
        token = data.get('token')
        if token and new_password:
            try:
                queryset = User.objects.filter(confirm_token=token)
                user = queryset.get()
                if user and user.is_confirm_token_expired():
                    queryset.update(confirm_token=None, confirm_token_expired_at=None,
                                    password=make_password(new_password))
                    #send_mail_on_password_reset(user)
            except User.DoesNotExist:
                pass

        #raise ResetPasswordFailed()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate(self, data):
        email = data.get('email')
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(email)
        pp.pprint('**********************************')
        if email:
            try:
                user = User.objects.filter(email=email).get()
                if user:
                    user.generate_token()
                    user.save()
                    #send_mail_on_frogot_password(user)
            except User.DoesNotExist:
                pass

        return []
