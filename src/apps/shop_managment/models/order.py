from django.db import models
from django.contrib.auth import get_user_model

from apps.core.behaviors import Authorable, Timestampable
from .product import Product


User = get_user_model()


class Order(Timestampable, Authorable):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    status = models.IntegerField(null=True, blank=True, default=1)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Order {self.id}'

    @property
    def total_cost(self):
        return sum(item.cost for item in self.items.all())


class OrderItem(Timestampable, Authorable):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'order')

    def __str__(self):
        return str(self.id)

    @property
    def cost(self):
        return (self.price or 0) * self.quantity
