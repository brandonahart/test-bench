"""
Description: This module opens a MongoDB and SQLite connection and
tests the execution time of equivalent queries

"""

import time
import csv
import sqlite3
from pymongo import MongoClient

# Create a connection to an in-memory SQLite database
conn = sqlite3.connect(":memory:")

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to import the data
cursor.execute("CREATE TABLE IF NOT EXISTS sports_data (Name TEXT, Code INTEGER, Sport TEXT, Letter TEXT, Number INTEGER)")

#conn.begin()

# Read the CSV file and insert the data into the table
with open("data.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        cursor.execute("INSERT INTO sports_data VALUES (?, ?, ?, ?, ?)", row)

# Commit the changes
#conn.commit()

cursor.execute("CREATE INDEX sports_data_sport on sports_data(Name, Sport)")
cursor.execute("EXPLAIN query plan SELECT Name, Sport, COUNT(*) FROM sports_data GROUP BY Name, Sport")
# Execute SQLite queries
start_time_sql = time.time()

#cursor.execute("SELECT Name, Sport, COUNT(*) FROM sports_data GROUP BY Name, Sport")
#cursor.execute("SELECT Name, Sport, avg(Number) as avg FROM sports_data GROUP BY Name, Sport")
cursor.execute("SELECT Name, Sport, avg(Number) as avg FROM sports_data GROUP BY Name, Sport order by Sport, Name")

rows = cursor.fetchall()
end_time_sql = time.time()
for row in rows:
    print(row)

execution_time_sql = end_time_sql - start_time_sql

print(f"SQLite execution time: {execution_time_sql:.2f} seconds\n")
print("\n")

#Same command with mongodb query
client = MongoClient("mongodb://localhost:27017/")
database = client["DirectDB"]
collection = database["collection1"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/
#collection.create_index([('Name', 1), ('Sport', 1)])
#pipeline = [
#    {
#        $group: {
#            _id: {
#                Name: "$Name",
#                Sport: "$Sport"
#            },
#            count: {
#                "$sum": 1
#            }
#        }
#    }, 
#    {
#        $project: {
#            Name: "$_id.Name",
#            Sport: "$_id.Sport",
#            count: 1,
#            _id: 0
#        }
#    }
#]
#
#start_time_mongo = time.time()
#cursor = collection.aggregate(
#    pipeline, 
#)
#end_time_mongo = time.time()
#try:
#    for doc in cursor:
#        print(doc)
#finally:
#    client.close()
#
#execution_time_mongo = end_time_mongo - start_time_mongo
#print(f"MongoDB execution time: {execution_time_mongo:.2f} seconds\n")
