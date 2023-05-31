'''
Module Name: ExportDB to ImportDB

Description: This module exports three collections from ExportDB and imports it
to another database ImportDB
'''

from pymongo import MongoClient

# Connect to the source MongoDB database
source_client = MongoClient('mongodb://localhost:27017')
source_db = source_client['ExportsDB']

# Connect to the destination MongoDB database
destination_client = MongoClient('mongodb://localhost:27017')
destination_db = destination_client['ImportsDB']

# Define the list of collections to export/import
collections_to_export = ['collection1', 'collection2', 'collection3']

for collection_name in collections_to_export:
    # Get the source collection
    source_collection = source_db[collection_name]
    
    # Get the documents from the source collection
    documents = source_collection.find()
    
    # Create the destination collection (if it doesn't exist)
    destination_collection = destination_db[collection_name]
    
    # Clear the destination collection (remove existing documents)
    destination_collection.delete_many({})
    
    # Insert the documents into the destination collection
    destination_collection.insert_many(documents)
    
    print(f"Successfully exported and imported collection: {collection_name}")

# Close the MongoDB connections
source_client.close()
destination_client.close()
