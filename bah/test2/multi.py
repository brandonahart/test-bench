import sqlite3
import multiprocessing
from pathlib import Path

# SQLite database file
database_file = "SQLite_Python.db"

# List of files to upload
files_to_upload = ["test1.txt", "test2.txt", "test3.txt"]

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create a table to store the files
cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        content BLOB
    )
""")
conn.commit()

# Function to upload a file as a BLOB
def upload_file(file_name):
    file_path = Path(file_name)

    with open(file_path, "rb") as file:
        file_content = file.read()

    cursor.execute("INSERT INTO files (filename, content) VALUES (?, ?)",
                   (file_name, file_content))
    conn.commit()

    print(f"Uploaded {file_name} successfully.")

# Main entry point
if __name__ == "__main__":
    # Upload files using multiprocessing
    with multiprocessing.Pool() as pool:
        pool.map(upload_file, files_to_upload)

    # Close the database connection
    conn.close()
