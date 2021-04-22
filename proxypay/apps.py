from django.apps import AppConfig

class ProxypayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proxypay'

    def ready(self):
        from . import signals