#!/usr/bin/python3

import redis
import uuid
from typing import Union, Callable, Optional

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
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], Union[str, int, float]]] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The Redis key to retrieve.
            fn (Callable): A function to convert the data to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved and optionally converted data.
        """
        value = self._redis.get(key)
        if value is None:
            return None  # Preserve Redis behavior for non-existent keys.
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a value as a UTF-8 string.

        Args:
            key (str): The Redis key to retrieve.

        Returns:
            Optional[str]: The retrieved value as a string or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve a value as an integer.

        Args:
            key (str): The Redis key to retrieve.

        Returns:
            Optional[int]: The retrieved value as an integer or None if the key does not exist.
        """
        return self.get(key, int)
