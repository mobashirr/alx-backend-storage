#!/usr/bin/python3

'''
    this module uses the redis which is in-memory data store system
    this system helpful cause its fast and reliable (data stored in RAM not in DISK)
    usually used for caching and session sotre purpose and more
    in this module i have just played with the basics of this technology
    by implemnting a chache class that intract with Radis client to store and retrive data from radis
    
    the count calls decorator used to detect how many time the method called its for monitoring porpuse
    __qualname__  special attribute that represents the qualified name of a function with full path (class.method etc)
    
'''

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method with call count functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to increment call count."""
        # Use the method's qualified name as the Redis key
        key = method.__qualname__
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data (str, bytes, int, float): The data to store.

        Returns:
            str: The random key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str) -> Optional[bytes]:
        """
        Retrieve a value from Redis.

        Args:
            key (str): The Redis key to retrieve.

        Returns:
            Optional[bytes]: The retrieved value or None if the key does not exist.
        """
        return self._redis.get(key)
