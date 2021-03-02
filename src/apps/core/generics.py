from rest_framework import generics, status
from rest_framework.response import Response
from .mixins import BulkDestroyModelMixin, BulkSoftDestroyModelMixin, BulkSoftRestoreModelMixin


class ActionViewBase(generics.GenericAPIView):

    serializer_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'kwargs': kwargs})
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class BulkDestroyModelView(BulkDestroyModelMixin, generics.GenericAPIView):
    """
    Bulk Destroy model instances.
    """

    def delete(self, request, *args, **kwargs):
        return self.bulk_destroy(request, *args, **kwargs)


class BulkSoftDestroyModelView(BulkSoftDestroyModelMixin, generics.GenericAPIView):
    """
    Bulk soft Destroy model instances.
    """

    def delete(self, request, *args, **kwargs):
        return self.bulk_soft_destroy(request, *args, **kwargs)


class BulkSoftRestoreModelView(BulkSoftRestoreModelMixin, generics.GenericAPIView):
    """
    Bulk soft restore model instances.
    """

    def delete(self, request, *args, **kwargs):
        return self.bulk_soft_restore(request, *args, **kwargs)
