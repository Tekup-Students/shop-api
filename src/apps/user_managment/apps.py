from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'apps.user_managment'
    label = 'user_managment'

    def ready(self):
        import apps.user_managment.signals
