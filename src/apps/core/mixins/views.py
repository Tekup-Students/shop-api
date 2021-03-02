from rest_framework import status
from rest_framework.response import Response


class BulkDestroyModelMixin:
    """
    Bulk Destroy model instances.
    """
    def bulk_destroy(self, request, *args, **kwargs):
        qs = self.get_queryset()
        filtered = self.filter_queryset(qs)
        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_bulk_destroy(self, objects):
        for obj in objects:
            obj.delete()


class BulkSoftDestroyModelMixin:
    """
    Bulk soft Destroy model instances.
    """

    def delete(self, request, *args, **kwargs):
        return self.bulk_soft_destroy(request, *args, **kwargs)

    def bulk_soft_destroy(self, request, *args, **kwargs):
        qs = self.get_queryset()
        filtered = self.filter_queryset(qs)
        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_bulk_soft_destroy(self, objects):
        for obj in objects:
            self.perform_destroy(obj)


class BulkSoftRestoreModelMixin:
    """
    Bulk soft restore model instances.
    """
    def bulk_soft_restore(self, request, *args, **kwargs):
        qs = self.get_queryset()
        filtered = self.filter_queryset(qs)
        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_bulk_soft_restore(self, objects):
        for obj in objects:
            self.perform_destroy(obj)
