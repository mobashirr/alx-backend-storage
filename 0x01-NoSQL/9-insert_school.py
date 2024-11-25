#!/usr/bin/python3

'''
insert based on **kwarg
'''


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a MongoDB collection based on kwargs.
    
    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: Key-value pairs representing the document to insert.
        
    Returns:
        The _id of the newly inserted document.
    """
    if not kwargs:
        raise ValueError("No data provided for insertion")
    
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
