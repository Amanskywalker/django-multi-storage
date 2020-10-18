# AWS S3 storage functions which is used accross the site
# Imports the AWS Boto3 library

import boto3
from botocore.exceptions import ClientError
import datetime

# Create a client for s3
s3_client = boto3.client('s3')

 def upload_to_s3(bucket_name, source_file, destination_name=None):
     """Upload a file to an S3 bucket

    :param source_file: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

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
