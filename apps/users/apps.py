from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'  # Ensure this matches your app's path

    def ready(self):
        # This import registers the signals when the app starts
        import apps.users.signals
