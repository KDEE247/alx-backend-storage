#!/usr/bin/env python3
"""web"""
import requests
import redis
from functools import wraps

# Connect to Redis
redis_client = redis.Redis()


def cache_with_expiry(expiration_time):
    """x"""
    def decorator(func):
        """"""
        @wraps(func)
        def wrapper(url):
            """"""
            # Create a key for counting accesses
            count_key = f"count:{url}"

            # Check if the URL is in cache
            cached_result = redis_client.get(url)
            if cached_result:
                # Increment access count
                redis_client.incr(count_key)
                return cached_result.decode('utf-8')

            # Make the request
            response = func(url)

            # Cache the result with expiration
            redis_client.setex(url, expiration_time, response)

            # Increment access count
            redis_client.incr(count_key)

            return response
        return wrapper
    return decorator


@cache_with_expiry(expiration_time=10)
def get_page(url: str) -> str:
    """track how many times a particular
       URL was accessed in the key"""
    response = requests.get(url)
    return response.text
