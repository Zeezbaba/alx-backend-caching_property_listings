from django.core.cache import cache
from .models import Property

def get_all_properties():
    # step 1: Check if its alreadt cached
    properties = cache.get('all_properties')

    # step 2: If not cached, fetch from db
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Step 3: Store in redis for 1hr (3600 seconds)
        cache.set('all_properties', properties, timeout=3600)
    else:
        print("Loaded from cache")

    return properties