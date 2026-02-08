from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    """
    Automatically creates a Cart instance whenever a new User is created.
    """
    if created:
        Cart.objects.get_or_create(user=instance)