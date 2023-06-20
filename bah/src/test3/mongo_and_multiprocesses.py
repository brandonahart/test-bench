import time
import csv
from pymongo import MongoClient
from multiprocessing import Pool

# MongoDB connection settings
mongodb_url = 'mongodb://localhost:27017'
database_name = 'TestDB'
collection_name = 'collection1'

# CSV file settings
csv_file = '../../../../../pythonTestPractice/student_data.csv'
delimiter = ','  # Change if your CSV file uses a different delimiter

# Number of worker processes
num_workers = 10  # Set the number of worker processes to utilize

# Connect to MongoDB

# Worker function to insert a batch of documents
def insert_batch(batch):
    collection.insert_many(batch)

# Function to process a chunk of the CSV file
def process_chunk(chunk):
    batch = []
    for row in chunk:
        batch.append(row)

        # Check if batch is full and insert into MongoDB
        if len(batch) == 500000:
            insert_batch(batch)
            batch = []

    # Insert any remaining documents in the last batch
    if batch:
        insert_batch(batch)


    # Connect to MongoDB
client = MongoClient(mongodb_url)
db = client[database_name]
collection = db[collection_name]
    
if __name__ == '__main__':
    start = time.time()
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=delimiter)
        rows = [row for row in csv_reader]

        # Determine the chunk size for each worker process
        total_rows = len(rows)
        chunk_size = total_rows // num_workers

        # Split the rows into chunks for each worker process
        chunks = [rows[i:i+chunk_size] for i in range(0, total_rows, chunk_size)]

        # Create a multiprocessing Pool and process the chunks in parallel
        with Pool(processes=num_workers) as pool:
            pool.map(process_chunk, chunks)

    # Close MongoDB connection
    end = time.time()
    ex = end - start
    print(f"Execution time in {ex} seconds")
    client.close()

