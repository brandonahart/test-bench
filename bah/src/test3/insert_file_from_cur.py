"""
Description: Module takes a csv file named data.csv from current directory
 and then uploads it to a mongodb collection called collection1

"""

import csv
from pymongo import MongoClient

# MongoDB connection settings
mongodb_url = 'mongodb://localhost:27017'
database_name = 'DirectDB'
collection_name = 'collection1'

# CSV file settings
csv_file = 'data.csv'
delimiter = ','  # Change if your CSV file uses a different delimiter

# Connect to MongoDB
client = MongoClient(mongodb_url)
db = client[database_name]
collection = db[collection_name]

# Open CSV file
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file, delimiter=delimiter)
    records = []
    for row in csv_reader:
        records.append(row)

    # Insert records into the MongoDB collection
    collection.insert_many(records)

# Close MongoDB connection
client.close()

