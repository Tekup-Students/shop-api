from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_active(self):
        return self.deleted_at is None


class Authorable(models.Model):
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    deleted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True
