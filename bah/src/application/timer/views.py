import csv
import time
import sqlite3
import os
import psutil
import boto3
from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .models import Upload
from .forms import UploadForm
from pymongo import MongoClient



# Home page index view function
def index(request):
    return HttpResponse("Hello, world. You're at the timer index.")

# Timer home page for timer app
def sleeping(request, name, count):
    time.sleep(count)
    return HttpResponse("Thank you for waiting, " + name + "\n")
    

# View function to upload a file
def upload_file(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            file_obj_type = str(type(file))
            if request.POST.get('choice') == 'DIRECTORY':
                print("Test for upload to directory")
                print(os.getenv('PUBLIC_KEY_ACCESS'))
                #Execute upload file
                header, start_time, ex_time, created_date, memory = handle_file_to_directory(file)

                #Use function to insert stats
                insert_stats(file, "fs", header, created_date, start_time, ex_time, memory[2], file_obj_type)

                #return form
                context = { "form": form, "ex_time": ex_time, "location": "file system", "memory": memory }
                return render(request, "timer/upload.html", context)

            elif request.POST.get('choice') == 'SQLITE':
                print("Test for upload to SQLite")
                #Execute upload file
                header, start_time, ex_time, created_date, memory = handle_file_to_sql(file)

                #Use function to insert stats
                insert_stats(file, "sql", header, created_date, start_time, ex_time, memory[2], file_obj_type)

                #return form
                context = { "form": form, "ex_time": ex_time, "location": "SQLite database", "memory": memory }
                return render(request, "timer/upload.html", context)

            elif request.POST.get('choice') == 'MONGO':
                print("Test for uplaod to MongoDB")
                #Execute upload file
                header, start_time, ex_time, created_date, memory = handle_file_to_mongo(file)
                
                #Use function to insert stats
                insert_stats(file, "mongo", header, created_date, start_time, ex_time, memory[2], file_obj_type)

                #return form
                context = { "form": form, "ex_time": ex_time, "location": "MongoDB", "memory": memory }
                return render(request, "timer/upload.html", context)

            elif request.POST.get('choice') == 'S3':
                print("Test for upload to S3")
                #Execute upload file
                header, start_time, ex_time, created_date, memory = handle_file_to_s3(file)

                #Use function to insert stats
                insert_stats(file, "s3", header, created_date, start_time, ex_time, memory[2], file_obj_type)

                #return form
                context = { "form": form, "ex_time": ex_time, "location": "S3", "memory": memory }
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

        header = func(*args, **kwargs)
        print(f"Header is: {header}")        

        end_time = time.time()
        ex_time = end_time - start_time
        created_date = datetime.now(timezone.utc)
        mem_after = process_memory()
        mem_output = (mem_before, mem_after, mem_after - mem_before)
        print("{}:consumed memory: {:}".format(
            func.__name__,
            mem_output))
        print(f"Time took to upload was {ex_time} seconds\n") 

        return (header, start_time, ex_time, created_date, mem_output)
    return wrapper


#Helper function to insert stats
def insert_stats(file, load_type, header, created_date, start_time, elapsed_time, memory_consumed, file_obj_type):
    connection = sqlite3.connect('../../data/stats.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS upload_stats (file_name TEXT, file_type TEXT, load_type TEXT, 
                     file_size INTEGER, header TEXT, created_date TEXT, start_time INTEGER, elapsed_time INTEGER, memory_consumed INTEGER, file_obj_type TEXT)""")

    insert_query = """INSERT INTO upload_stats 
                      (file_name, file_type, load_type, file_size, header, created_date, start_time, elapsed_time, memory_consumed, file_obj_type)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    data_tuple = (file.name, file.content_type, load_type, file.size, header, created_date, start_time, elapsed_time, memory_consumed, file_obj_type)
    cursor.execute(insert_query, data_tuple)
    
    print("File stats inserted")
    connection.commit()
    cursor.close()

# Helper view function to handle regular file upload to specific loaction
@profiler
def handle_file_to_directory(f):
    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)
    with open("../../data/uploads-django/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return header


#Helper function to stream file into mongodb
@profiler
def handle_file_to_mongo(f):
    client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = client[settings.MONGODB_DATABASE]
    collection = db[settings.MONGODB_COLLECTION]

    header = f.readline().decode('utf-8').stript('\n')
    f.seek(0)    
    
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
    return header


#Helper function to stream file into sqlite
@profiler
def handle_file_to_sql(f):
    connection = sqlite3.connect('../../data/SportsDB.db')
    cursor = connection.cursor()

    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)    

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
    return header


@profiler
def handle_file_to_s3(f):
    print(type(f))

    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)

    s3 = boto3.client('s3', aws_access_key_id=settings.PUBLIC_KEY, aws_secret_access_key=settings.PRIVATE_KEY)
    file_name = "s3_test_{}".format(datetime.now(timezone.utc))   

    s3.put_object(Body=f, Bucket="bahbucket", Key=file_name)
    
    return header


