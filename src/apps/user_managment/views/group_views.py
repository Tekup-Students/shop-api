from django.db.models import Q
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import Permission, Group
from django.conf import settings

from apps.core.generics import BulkDestroyModelView
from ..serializers import PermissionSerializer, GroupSerializer


class GroupListCreateAPIView(generics.ListCreateAPIView, BulkDestroyModelView):
    """
       List of Groups.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    search_fields = (
        'name',
    )
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['pk']

    def create(self, request, *args, **kwargs):
        data = request.data
        permissions = data.pop('permissions', None)
        if permissions:
            permissions = Permission.objects.filter(codename__in=permissions).values_list('id', flat=True)
            data.update(permissions=permissions)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ALLGroupListAPIView(generics.ListAPIView):
    """
       List of ALL Groups.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    pagination_class = None


class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update a Role.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        permissions_codename = instance.permissions.all().values_list('codename', flat=True)
        data.update(permissions=permissions_codename)
        return Response(data)

    def update(self, request, *args, **kwargs):
        data = request.data
        permissions = data.pop('permissions', None)
        if permissions:
            permissions = Permission.objects.filter(codename__in=permissions).values_list('id', flat=True)
            data.update(permissions=permissions)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
