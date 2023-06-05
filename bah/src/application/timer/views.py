import csv
import time
import sqlite3
import os
import psutil
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .models import Upload
from .forms import UploadFileForm
from .forms import UploadForm
from pymongo import MongoClient



# Home page index view function
def index(request):
    return HttpResponse("Hello, world. You're at the timer index.")

def sleeping(request, name, count):
    time.sleep(count)
    return HttpResponse("Thank you for waiting, " + name + "\n")
    

# View function to upload a file
def upload_file(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('choice') == 'DIRECTORY':
                print("Test for upload to directory")
                ex_time, result = handle_file_to_directory(request.FILES["file"])
                context = { "form": form, "ex_time": ex_time, "location": "file system", "memory": result }
                return render(request, "timer/upload.html", context)

            elif request.POST.get('choice') == 'SQLITE':
                print("Test for upload to SQLite")
                ex_time, result = handle_file_to_sql(request.FILES["file"])
                context = { "form": form, "ex_time": ex_time, "location": "SQLite database", "memory": result }
                return render(request, "timer/upload.html", context)

            elif request.POST.get('choice') == 'MONGO':
                print("Test for uplaod to MongoDB")
                ex_time, result = handle_file_to_mongo(request.FILES["file"])
                context = { "form": form, "ex_time": ex_time, "location": "MongoDB", "memory": result }
                return render(request, "timer/upload.html", context)

            else:
                return HttpResponse("File Uploaded no where")
    else:
        form = UploadForm()
    return render(request, "timer/upload.html", {"form": form})


#inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


#Decorator function
def profiler(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        mem_before = process_memory()
        result = func(*args, **kwargs)
        end_time = time.time()
        ex_time = end_time - start_time
        mem_after = process_memory()
        mem_output = (mem_before, mem_after, mem_after - mem_before)
        print("{}:consumed memory: {:}".format(
            func.__name__,
            mem_output))
        print(f"Time took to upload was {ex_time} seconds\n") 
        return (ex_time, mem_output)
    return wrapper


# Helper view function to handle regular file upload to specific loaction
@profiler
def handle_file_to_directory(f):
    with open("../../data/uploads-django/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


#Helper function to stream file into mongodb
@profiler
def handle_file_to_mongo(f):
    client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = client[settings.MONGODB_DATABASE]
    collection = db[settings.MONGODB_COLLECTION]

    # Read and insert CSV data into MongoDB
    csv_reader = csv.DictReader(f.read().decode('utf-8').splitlines())
    documents = []
    for row in csv_reader:
        documents.append(row)
        if len(documents) >= 500000:  # Adjust batch size as needed
            collection.insert_many(documents)
            documents = []

    # Insert remaining documents
    if documents:
        collection.insert_many(documents)
    client.close()


#Helper function to stream file into sqlite
@profiler
def handle_file_to_sql(f):
    connection = sqlite3.connect('../../data/SportsDB.db')
    cursor = connection.cursor()

    csv_data = f.read().decode('utf-8').splitlines()
    reader = csv.reader(csv_data)
    column_names = next(reader)
    columns = ", ".join(column_names)

    table_name = 'sports_data'
    cursor.execute("drop table if exists sports_data")
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    cursor.execute(create_table_query)

    placeholders = ", ".join('?' for _ in column_names)
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    
    data = [tuple(row) for row in reader]
    
    cursor.executemany(insert_query, data)

    connection.commit()
    connection.close()

