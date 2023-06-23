from concurrent.futures import ThreadPoolExecutor
import csv
import time
import sqlite3
import psutil
import boto3
from datetime import datetime, timezone
from django.core.paginator import Paginator
from botocore.exceptions import NoCredentialsError
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from .models import Upload
from .forms import UploadFileForm, UploadMultiFileForm
from pymongo import MongoClient

from django.contrib.auth.decorators import login_required


# Home page index view function
@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'timer_index.html', context)
    #return HttpResponse("Hello, world. You're at the timer index. Add links including 'Upload One File' 'Upload Multiple Files' 'Check Uploaded Files Stats'")


# View function to upload a file
@login_required(login_url='login')
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            location = form.cleaned_data['location']
            
            start_time = time.time()
            memory_usage = psutil.Process().memory_info().rss

            if location == 'DIRECTORY':
                header = handle_file_to_directory(file)
            elif location == 'SQLITE':
                header = handle_file_to_sql(file)
            elif location == 'MONGO':
                header = handle_file_to_mongo(file)
            elif location == 'S3':
                header = handle_file_to_s3(file)
    
            elapsed_time = time.time() - start_time
            create_date = datetime.now(timezone.utc)
            memory_consumed = (psutil.Process().memory_info().rss - memory_usage) / (1024 * 1024)

            # Create a new UploadedFile instance and save it to the database
            uploaded_file = Upload(
                file_name = file.name,
                file_type = file.content_type,
                load_type = location,
                file_size = file.size,
                header = header,
                create_date = create_date,
                start_time = start_time,
                elapsed_time = elapsed_time,
                memory_consumed = memory_consumed,
                file_obj_type = str(type(file))
            )
            uploaded_file.save()

            return redirect('/timer/files/')

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


#Handles multiple file upload
@login_required(login_url='login')
def upload_multiple_files(request):
    if request.method == 'POST':
        form = UploadMultiFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        s3 = boto3.client('s3',aws_access_key_id=settings.PUBLIC_KEY, aws_secret_access_key=settings.PRIVATE_KEY)
        bucket_name = 'bahbucket'

        try:
            uploaded_files = []
            futures = []

            with ThreadPoolExecutor(max_workers=3) as executor:
                for file in files:
                    key = 'uploads/' + file.name  # Key under which the file will be stored in the bucket

                    future = executor.submit(
                        s3.upload_file,
                        file.temporary_file_path(),
                        bucket_name,
                        key
                    )
                    futures.append(future)

                # Wait for all futures to complete
                for future in futures:
                    future.result()

                    # Generate the file URL using Transfer Acceleration
                    file_url = f"https://{bucket_name}.s3-accelerate.amazonaws.com/{key}"
                    uploaded_files.append({'name': file.name, 'url': file_url})

            return HttpResponse('Files were uploaded successfully')
        except NoCredentialsError:
            return HttpResponse('AWS credentials not found. Please configure AWS CLI.')
    else:
        form = UploadMultiFileForm()    
    return render(request, 'multi_upload.html', {'form': form})


# View function to display file stats table
@login_required(login_url='login')
def file_list(request):
    files = Upload.objects.all()
    return render(request, 'file_list.html', {'files': files})


# View function to display contents of specific file in pages
def csv_table_view(request):
    # Connect to the SQLite database
    connection = sqlite3.connect('../../data/SportsDB.db')
    cursor = connection.cursor()
    table_name = 'sports'

    # Fetch the column names from the SQLite table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
    columns = [column[0] for column in cursor.description]
    print(columns)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')
    # Set the number of rows to display per page
    rows_per_page = 10
    
    if page_number:
        index = (int(page_number) - 1) * rows_per_page
        # Fetch only the 10 rows for the current page
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {rows_per_page}, OFFSET {index}")
    else:
        # Fetch the first 10 rows for the initial page
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {rows_per_page}")

    # Fetch the rows from the cursor
    rows = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Create a Paginator object with the rows and the desired number of rows per page
    paginator = Paginator(rows, rows_per_page)

    # Get the Page object for the current page number
    page = paginator.get_page(page_number)
    print(page,page.has_next,page.has_previous)

    # Pass the page object to the template for rendering
    return render(request, 'preview.html', {'page': page, 'columns': columns})


# Helper view function to handle regular file upload to specific loaction
def handle_file_to_directory(f):
    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)
    with open("../../data/uploads-django/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return header

#Helper function to stream file into mongodb
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
def handle_file_to_sql(f):
    connection = sqlite3.connect('../../data/SportsDB.db')
    cursor = connection.cursor()

    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)    

    csv_data = f.read().decode('utf-8').splitlines()
    reader = csv.reader(csv_data)
    column_names = next(reader)
    columns = ", ".join(column_names)

    table_name = '' + f.name + 'x'
    drop_table_query = "DROP TABLE IF EXISTS sports"
    cursor.execute(drop_table_query)
    create_table_query = 'CREATE TABLE sports ({})'.format(columns)
    cursor.execute(create_table_query)

    placeholders = ", ".join('?' for _ in column_names)
    insert_query = 'INSERT INTO sports VALUES ({})'.format(placeholders)
    
    data = [tuple(row) for row in reader]
    
    cursor.executemany(insert_query, data)

    connection.commit()
    connection.close()
    return header

#Helper function to stream file into s3
def handle_file_to_s3(f):
    print(type(f))

    header = f.readline().decode('utf-8').strip('\n')
    f.seek(0)

    s3 = boto3.client('s3', aws_access_key_id=settings.PUBLIC_KEY, aws_secret_access_key=settings.PRIVATE_KEY)
    file_name = "s3_test_{}".format(datetime.now(timezone.utc))   

    s3.put_object(Body=f, Bucket="bahbucket", Key=file_name)
    
    return header
