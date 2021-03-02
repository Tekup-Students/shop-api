from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.order import OrderItem

@receiver(post_save, sender=OrderItem)
def save_order_item(sender, instance, created, **kwargs):
    if created:
        instance.price = instance.product.price
        instance.save()
