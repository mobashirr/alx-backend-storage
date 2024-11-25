#!/usr/bin/env python3
'''
list all module
'''


def list_all(mongo_collection):
    '''
    list all docs of collection

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        empty list if no document in the collection

    '''
    results = mongo_collection.find()
    return results
