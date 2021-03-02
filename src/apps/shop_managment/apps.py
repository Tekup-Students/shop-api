from django.apps import AppConfig


class ShopManagmentConfig(AppConfig):
    name = 'apps.shop_managment'
    label = 'shop_managment'

    def ready(self):
        import apps.shop_managment.signals
