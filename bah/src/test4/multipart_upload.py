import time
import boto3
from boto3.s3.transfer import TransferConfig

ACCESS_KEY = 'AKIAUWKA3JWNWF7HVK6Y'
SECRET_KEY = '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'
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def uploadFileS3(filename, bucket, s3filename):
    config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
                        multipart_chunksize=1024*25, use_threads=True)
    
    s3_client.upload_file(filename, bucket, s3filename, Config = config)


start = time.time()
uploadFileS3('../../data/data.csv', 'bahbucket', 'data.csv')
end = time.time()
ex = end - start
print(f"Execution time was {ex} seconds")
