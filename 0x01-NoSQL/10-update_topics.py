#!/usr/bin/env python3
'''
update topics
'''

def update_topics(mongo_collection, name, topics):
    '''
    update a document based on given name

    Args:
        mongo_collection: The pymongo collection object.
        name: name which we want to change 
        topics: (list of strings) will be the list of topics approached in the school

    Returns: number of modyfied docs
    '''
    result = mongo_collection.update_many(
        {'name':name},
        {'$set':{'topics':topics}}
    )
    return result.modified_count
