"""
Module Name: Auto Generate Mongo Data

Description: This module auto generates a number of documents into a table
with specific columns

"""
import pymongo
import string
import random
import datetime

# MongoDB connection
client = pymongo.MongoClient('localhost', 27017)
db = client['TestDB']
collection = db['TestCollection']

# List of catagories
catagories = ["A", "B", "C", "D", "E"]

# Number of documents to insert
num_docs = 1000

# Generate and insert docs
docs = []
for _ in range(num_docs):
    random_int = random.randint(1,100)
    random_catagory = random.choice(catagories)
    timestamp = datetime.datetime.now()
    document = {
        "random_int": random_int,
        "random_catagory": random_catagory,
        "timestamp": timestamp
    }
    docs.append(document)


# Insert docs into collection
collection.insert_many(docs)

# close connection
client.close()
