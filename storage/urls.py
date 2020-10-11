'''
    storage module URL Configuration
'''

from django.urls import include, path
from storage.views import (
    FileDownload,
    FileUpload
)

urlpatterns = [
    path('upload', FileUpload.as_view(), name='file_upload'),
    path('url/<int:fid>', FileDownload.as_view(), name='file_upload'),
]

