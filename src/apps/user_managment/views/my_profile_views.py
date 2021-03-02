from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import CurrentProfileSerializer, UpdateCurrentPasswordSerializer
from apps.core.generics import ActionViewBase


class MyProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrentProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        user = data.get('user', None)
        if user and user.get('email', None) == instance.user.email:
            user.pop('email', None)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MyProfileUpdatePasswordAPIView(ActionViewBase):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateCurrentPasswordSerializer
