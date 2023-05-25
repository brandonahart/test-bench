"""
    Test connecting to mongo using pymongo driver
"""

from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017")


db = client.testA
collection = db.junk

doc = {"name": "secret", "text": "xyzzy", "cdate": datetime.datetime.utcnow()}

junk = db.junk
nid = junk.insert_one(doc).inserted_id

print("Id:" + str(nid))


