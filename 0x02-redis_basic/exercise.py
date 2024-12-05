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


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    
    # Retrieve all inputs and outputs from Redis
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)
    
    # Print the header
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    
    # Zip inputs and outputs together and print them
    for input_data, output_data in zip(inputs, outputs):
        # Convert byte strings back to regular strings (input_data is a byte string)
        input_data = input_data.decode("utf-8")
        output_data = output_data.decode("utf-8")
        
        # Print the formatted output
        print(f"{method.__qualname__}({input_data}) -> {output_data}")


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
