from django.apps import AppConfig

class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'

    def ready(self):
        # This import is vital; it connects the signal
        import apps.cart.signals