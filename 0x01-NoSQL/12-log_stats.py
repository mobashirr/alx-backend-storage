#!/usr/bin/env python3

'''
Python script that provides some stats about Nginx logs stored in MongoDB:
'''


from pymongo import MongoClient


def nginx_stats():
    """
    Displays statistics about Nginx logs stored in MongoDB.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    nginx_collection = db['nginx']

    # Get total number of logs
    total_logs = nginx_collection.count_documents({})

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: nginx_collection.count_documents({"method": method}) for method in methods}

    # Count GET requests to /status
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})

    # Display stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    nginx_stats()
