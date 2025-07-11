from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

# signal when property is created or updated
@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    print("Property saved - clearing redis cache")
    cache.delete('all_properties')

# signal when property is deleted
@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    print("Property deleted - clearing redis cache")
    cache.delete('all_properties')