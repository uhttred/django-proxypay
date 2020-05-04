from django.apps import AppConfig

class ProxypayConfig(AppConfig):
    # application name
    name = 'proxypay'

    def ready(self):
        # importing signal
        from . import signals