from django.db import models
from apps.core.behaviors import Authorable, Timestampable


class Category(Timestampable, Authorable):
    
    category_name = models.CharField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.category_name}"

