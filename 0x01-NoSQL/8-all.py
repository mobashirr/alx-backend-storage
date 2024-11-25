#!/usr/bin/python3

def list_all(mongo_collection):
    return mongo_collection.find()