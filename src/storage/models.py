from django.contrib.auth import get_user_model

from django.contrib.gis.db import models

class FileStorage(models.Model):
    '''
    Stored the data and location related to the files uploaded to the buckets
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashed_name = models.CharField(max_length=255, unique=True)     # unique name for the file after hashing use for identification
    original_name = models.CharField(max_length=255)
    original_meta_data = models.TextField(null=True)
    original_size = models.IntegerField(null=True, help_text='The size, in bytes, of the uploaded file.')
    original_charset = models.CharField(max_length=255, null=True)
    bucket_raw = models.CharField(max_length=255, null=True)
    bucket_name = models.CharField(max_length=255, null=True)
    server_reply = models.TextField(null=True)                      # server reply after storing the object

class FileTransactionLogs(models.Model):
    '''
    Stored the file storage and its transaction logs
    '''
    file = models.ForeignKey(FileStorage, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True)