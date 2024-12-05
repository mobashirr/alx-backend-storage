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
from typing import Callable

def call_history(method: Callable) -> Callable:
    """
    Decorator to store function input arguments and output in Redis.
    
    Args:
        method (Callable): The method to decorate.
        
    Returns:
        Callable: The decorated method.
    """
    def wrapper(self, *args, **kwargs):
        """Wrap the method to store call history."""
        # Use the method's qualified name to form keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Normalize the input arguments (since Redis only stores strings, bytes, or numbers)
        self._redis.rpush(input_key, str(args))  # Append inputs to the inputs list
        # Call the original method and store its result
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))  # Append outputs to the outputs list
        return result
    
    return wrapper

class Cache:
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: str) -> str:
        """
        Store data in Redis with a random key.
        
        Args:
            data (str): The data to store.
            
        Returns:
            str: The random key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
