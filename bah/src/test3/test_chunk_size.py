"""
Description: Module uses multiprocessing and insert_many

"""


import time
from pymongo import MongoClient
from multiprocessing import Pool
from functools import partial

# MongoDB connection settings
mongodb_url = "mongodb://localhost:27017"
database_name = "ChunkSizeDB"
collection_name = "testcollection"

# Number of documents to generate and insert
num_documents = 10000000

# Chunk sizes to test
chunk_sizes = [50000, 100000, 500000, 1000000, 2000000, 3000000]

# Function to generate a sample document
def generate_document(index):
    return {"index": index, "name": f"Document {index}"}

# Function to insert a chunk of documents
def insert_chunk(chunk, mongodb_url, database_name, collection_name):
    client = MongoClient(mongodb_url)
    db = client[database_name]
    collection = db[collection_name]
    collection.insert_many(chunk)
    client.close()

# Function to insert documents with a specified chunk size
def insert_documents(chunk_size):
    client = MongoClient(mongodb_url)
    db = client[database_name]
    collection = db[collection_name]

    documents = [generate_document(i) for i in range(num_documents)]
    chunks = [documents[i:i + chunk_size] for i in range(0, num_documents, chunk_size)]

    start_time = time.time()

    with Pool() as pool:
        pool.map(partial(insert_chunk, mongodb_url=mongodb_url, database_name=database_name, collection_name=collection_name), chunks)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Chunk size: {chunk_size}, Execution time: {execution_time:.2f} seconds")

    client.close()

if __name__ == '__main__':
    # Insert documents with different chunk sizes and measure execution time
    for chunk_size in chunk_sizes:
        insert_documents(chunk_size)
