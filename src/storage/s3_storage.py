# AWS S3 storage functions which is used accross the site
# Imports the AWS Boto3 library

import boto3
from botocore.exceptions import ClientError
import datetime

# Create a client for s3
s3_client = boto3.client("s3")


def upload_to_s3(bucket_name, source_file, destination_name=None):
    """Upload a file to an S3 bucket

    :param source_file: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False"""

    # If S3 object_name was not specified, use file_name

    if destination_name is None:
        destination_name = file_name

    try:
        response = s3_client.upload_file(source_file, bucket_name, destination_name)
        print(
            "File {} uploaded to bucket {} at {}".format(
                source_file, bucket_name, destination_name
            )
        )
    except ClientError as e:
        print(e)
        return False

    return True


def create_presigned_url_s3(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    bucket_name: string
    object_name: string
    expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response


## Listing all objects in the Bucket
def list_files_in_bucket(bucket_name):
    """
    List all files in bucket
    """
    try:
        response = client.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        print(e)
        return None

    for key in response["Contents"]:
        print("-> {}".format(key["Key"]))


def download_from_s3(bucket_name, object_name, file_name):
    try:
        s3_client.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        print(e)
        return None
