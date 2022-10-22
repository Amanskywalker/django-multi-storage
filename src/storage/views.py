from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from storage.helper import Storage


class FileUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        basic funtion to upload the file

        need to pass the file upload location (mainly the bucket name) too
        """
        storage = None
        # check name data is provided or not
        if request.POST:
            # mount the bucket specified in request
            storage = Storage(request.POST["name"])
        else:
            # mount the default bucket
            storage = Storage()
        # check file data is provided
        if request.FILES:
            # file data is provided then proced the upload the file
            file_data = request.FILES["file"]
            # upload the file
            file_details = storage.save_file(request=request, file=file_data)
            # return the file hash
            if file_details["status"]:
                return Response({"file": file_details["file"].hashed_name}, status=200)
            else:
                return Response({"error": file_details["error"]}, status=400)
        else:
            # file is not provided so return the error code
            return Response({"error": "Unsupported Media Type"}, status=415)

        # By default return the method is not allowed as something is wrong
        return Response({"error": "Method Not allowed"}, status=405)


class FileDownload(APIView):
    """
    Download the file from the server based on the fid which is provided
    """

    def get(self, request, fid):
        storage = Storage()
        storage.get_object_url(object_id=fid)
        return Response({"file": "ok"}, status=200)
