from django.db import models

from apps.core.behaviors import Authorable, Timestampable
from .category import Category


class Product(Timestampable, Authorable):
    
    product_image = models.ImageField()
    product_name = models.CharField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.RESTRICT)
    
    @property
    def available(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.product_name}"


class ProductImage(Timestampable, Authorable):

    product = models.ForeignKey(Product, related_name='images', on_delete=models.RESTRICT)
    image = models.ImageField()

