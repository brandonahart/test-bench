"""
Module Name: PyMongo test1

Description: This module was used as a test to create a simple collection and learn how to insert and find data
"""

from pymongo import MongoClient

# Create the client
client = MongoClient('localhost', 27017)

# Connect to our database
db = client['SeriesDB']

# Fetch our series collection
collection = db['series']

#post1 = {"_id": 0, "name": "brandon", "score": 5}

print(collection.find_one())
