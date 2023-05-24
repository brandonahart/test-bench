"""
Module Name: Data Insertion

Description: This module inserts records into two different MongoDB
collections concurrently using multiprocessing

"""
import pymongo
from multiprocessing import Process

# MongoDB connection settings
mongo_host = 'localhost'
mongo_port = 27017
mongo_database = 'SeriesDB'

# Number of records to insert
N = 100

def insert_records(collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_database]
    collection = db[collection_name]

    # Generate records
    records = [{'data': f'Record {i+1} in {collection_name}'} for i in range(N)]

    # Insert records
    collection.insert_many(records)

    # Close the connection within the subprocess
    client.close()

if __name__ == '__main__':
    # Fork Process A
    process_a = Process(target=insert_records, args=('SeriesA',))
    process_a.start()

    # Fork Process B
    process_b = Process(target=insert_records, args=('SeriesB',))
    process_b.start()

    # Wait for both processes to finish
    process_a.join()
    process_b.join()

    print('Records inserted successfully.')
