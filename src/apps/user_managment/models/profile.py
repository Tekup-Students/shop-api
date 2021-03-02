from django.db import models
from django.contrib.auth import get_user_model

from apps.core.behaviors import Authorable, Timestampable

User = get_user_model()


class Profile(Timestampable, Authorable):
    """Profile"""
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
