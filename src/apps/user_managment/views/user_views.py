import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.filters import RelatedOrderingFilter
from django.contrib.auth import get_user_model

from ..models import Profile
from ..serializers import ProfileSerializer, SimpleUserSerializer

User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user').all()

    search_fields = (
        'phone',
        'second_phone',
        # user filter
        'user__first_name',
        'user__last_name',
        'user__email',
    )
    filter_backends = [filters.SearchFilter, RelatedOrderingFilter]
    ordering_fields = '__all__'
    ordering = ['pk']

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        filter_kwargs = {'user__is_superuser': False}
        is_active = self.request.query_params.get('is_active', None)
        if is_active:
            try:
                is_active = int(is_active)
                filter_kwargs.update(deleted_at__isnull=is_active)
            except ValueError:
                pass
        return qs.filter(**filter_kwargs)


class ALLUserListAPIView(generics.ListAPIView):
    """
       List of ALL users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer
    queryset = User.objects.filter(is_active=True,)
    pagination_class = None


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(deleted_at__isnull=True, user__is_superuser=False)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        user = data.get('user', None)
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(data)
        pp.pprint(instance.user.email)
        pp.pprint('**********************************')
        if user and user.get('email', None) == instance.user.email:
            user.pop('email', None)

        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(data)
        pp.pprint('**********************************')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        deleted_at__isnull=True,
        user__is_superuser=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.user.is_active = False
        instance.user.save()
        instance.save()


class UserActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        deleted_at__isnull=False,
        user__is_superuser=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.user.is_active = True
        instance.user.save()
        instance.save()
