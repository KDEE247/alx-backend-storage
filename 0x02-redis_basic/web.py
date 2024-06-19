#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''
store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@data_cacher
@count_url_access
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
