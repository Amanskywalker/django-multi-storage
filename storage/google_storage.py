# GCP storege functions which is used accross the site
# Imports the Google Cloud client library
from google.cloud import storage
import datetime

# Instantiates a client
storage_client = storage.Client.from_service_account_json('config/gcp_storage.json')

def upload_blob(bucket_name, source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    
    # bucket to upload
    bucket = storage_client.bucket(bucket_name)
    # final name of the blob
    blob = bucket.blob(destination_blob_name)
    #upload the bolb
    # result = blob.upload_from_filename(source_file_name)
    result = blob.upload_from_file(
        source_file,
        content_type=str(source_file.content_type))
    print(result)
    print(
        "File {} uploaded to {}".format(
            source_file, destination_blob_name
        )
    )
    return True

def generate_download_signed_url_v4(bucket_name, blob_name):
    """
    Generates a v4 signed URL for downloading a blob.
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=30),
        # Allow GET requests using this URL.
        method="GET",
    )

    return url