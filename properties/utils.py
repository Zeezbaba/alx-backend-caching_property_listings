from django.core.cache import cache
from django_redis import get_redis_connection
import logging
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

def get_redis_cache_metrics():
    # Get redis connection used by django redis
    redis_conn = get_redis_connection('default')

    # Get server info
    info = redis_conn.info()

    # Extract the hit and misses
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    # Calculate hits ratio safely
    total = hits + misses
    if total == 0:
        hit_ratio = 0.0
    else:
        hit_ratio = hits / total

    # Log the info for debugging
    logging.info(f"Redis Cache Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

    # Return a dictionary of metrics
    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }