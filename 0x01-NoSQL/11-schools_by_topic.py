#!/usr/bin/env python3
'''
schools by topic
'''


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic:
    
    Args:
        mongo_collection: The pymongo collection object.
        topic: (string) will be topic searched
        
    Returns:
        list of school having a specific topic:
    """
    result = mongo_collection.find({'topic':topic})
    return list(result) # return a list from the cursor
