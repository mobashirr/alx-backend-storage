#!/usr/bin/python3


import redis
import uuid
from typing import Union

class Cache:
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.
        
        Args:
            data (str, bytes, int, float): The data to store.

        Returns:
            str: The random key used to store the data.
        """
        # Generate a random UUID-based key
        key = str(uuid.uuid4())
        # Store the data in Redis
        self._redis.set(key, data)
        return key
