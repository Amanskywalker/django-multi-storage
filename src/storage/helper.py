from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import hashlib
import json

try:
    import libcloud
except ImportError:
    raise ImproperlyConfigured("Could not load libcloud")


try:
    from django.utils.six.moves.urllib.parse import urljoin
except ImportError:
    string_types = str
    from urllib.parse import urljoin

from storage.models import FileStorage, FileTransactionLogs

provider_mapper = {
    "google_storage": libcloud.DriverType.STORAGE.GOOGLE_STORAGE,
}


class Storage:
    """
    Storage class to abstract the storage function accross the multiple service providers
    """

    # hold the drive then main connection the provider
    driver = None
    # hold the provider data
    provider = settings.STORAGE_PROVIDERS["default"]
    # hold the bucket data
    bucket = None

    # initilize the class
    def __init__(self, provider_name=None):
        """Establish the connection.

        __init__ establish the connection with the provider and connect to the bucket.

        Parameters
        ----------
        provider_name : string
            it should be the configuration key which is defined in the settings file

        Returns
        -------
        None
            It updated the object connection parameter

        Raises
        ------
        ImproperlyConfigured
            When the configuration is not proper


        Examples
        --------
        >>> s=Storage('default')
        """
        # check if the provider name is in the list or none
        if provider_name is not None:
            # build the provider dict
            self.provider = settings.STORAGE_PROVIDERS[provider_name]

        try:
            # load the connection driver
            cls = libcloud.get_driver(
                libcloud.DriverType.STORAGE, provider_mapper[self.provider["type"]]
            )
        except Exception as e:
            # if connection driver is not found, raise an expection
            raise ImproperlyConfigured(
                "Unable to find libcloud driver type %s: %s"
                % (provider_mapper[self.provider["type"]], e)
            )

        try:
            # make the connection with the platform, pass the username and secret
            self.driver = cls(key=self.provider["user"], secret=self.provider["secret"])
            # connect to the bucket, only one bucket connection is allowed per connection
            self.bucket = self.driver.get_container(self.provider["bucket"])
        except Exception as e:
            # if connection to bucket is not established then raise an expection
            raise ImproperlyConfigured(
                "Unable to create libcloud driver type %s: %s"
                % (provider_mapper[self.provider["type"]], e)
            )

    def hash_file(self, file_data, hash_algo=None):
        """Hash the file

        Funtion to generate the hash sha3_512 hash of the given file

        Parameters
        ----------
        file_data : File
            The File which need to be hashed, it should be inMemory file
        hash_algo : string
            Name of the hashing algorithm need to be use
            (supported algorithms : md5,)

        Returns
        -------
        srting
            Hash digest of the file

        Raises
        ------
        AttributeError
            The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        """
        # Create the hash object
        file_hash = hashlib.sha3_512()
        # Open the file to read it's bytes
        for f in file_data.chunks():
            # Update the hash
            file_hash.update(f)

        # Retun the hexadecimal digest of the hash
        return file_hash.hexdigest()

    def list_container_objects(self):
        """
        Return a list of objects for the given (in setting) container.
        """
        return self.driver.list_container_objects(self.bucket)

    def list_containers(self):
        """
        Return a list of containers.
        """
        return self.driver.list_containers()

    def save_file(self, request, file):
        # create the return object
        reply = {
            "status": False,
            "error": "None",
            "file": None,
        }

        # create hash of the file
        file_hash = self.hash_file(file)

        # upload the file
        try:
            server_reply = self.upload_object(file=file, file_name=file_hash)
        except Exception as e:
            # update the error and return
            reply["error"] = "error Uploading the file :" + str(e)
            return reply

        # try saving the file related data to DB
        try:
            file_data = FileStorage.objects.create(
                hashed_name=self.hash_file(file),
                original_name=file.name,
                original_meta_data=file.content_type,
                original_size=file.size,
                original_charset=file.charset,
                bucket_raw=self.bucket,
                bucket_name=self.bucket.name,
                server_reply=server_reply,
            )
        except Exception as e:
            # update the error and return
            reply["error"] = "error Saving file data in DB :" + str(e)
            return reply

        # try saving the file transaction log
        try:
            FileTransactionLogs.objects.create(
                file=file_data,
                user=request.user,
                remark="File uploaded",
            )
        except Exception as e:
            # update the error and return
            reply["error"] = "error Saving file transaction data :" + str(e)
            return reply

        reply["file"] = file_data
        reply["status"] = True
        return reply

    def upload_object(self, file, file_name):
        """
        upload the file to bucket
        """
        return self.driver.upload_object_via_stream(
            iterator=file.chunks(),
            container=self.bucket,
            object_name=file_name,
            extra={
                "meta_data": {
                    "content_type": file.content_type,
                }
            },
        )

    def get_object_url(self, object_data=None, object_id=None, object_hash=None):
        """
        Return the object URL based on the id of the object from the storage table
        """
        object_details = None
        # get the object from the database
        try:
            if object_data is not None:
                object_details = object_data
            elif object_id is not None:
                object_details = FileStorage.objects.get(id=object_id)
            elif object_hash is not None:
                object_details = FileStorage.objects.get(hashed_name=object_hash)
        except Exception as e:
            error = "No object found" + str(e)
            print(error)

        # connect to the object bucket
        if self.mount_driver_from_bucket_name(bucket_name=object_details.bucket_name):
            print("bucket connected")
        else:
            error = "No bucket found"
            print(error)

        # get the object
        object_blob = self.driver.get_object(
            container_name=self.bucket.name, object_name=object_details.hashed_name
        )

        # get the object URL
        try:
            url = self.driver.get_object_cdn_url(object_blob)
        except NotImplementedError as e:
            object_path = "{}/{}".format(self.bucket.name, object_blob.name)
            if "s3" in self.provider["type"]:
                base_url = "https://%s" % self.driver.connection.host
                url = urljoin(base_url, object_path)
            elif "google" in self.provider["type"]:
                url = urljoin("https://storage.googleapis.com", object_path)
            else:
                raise e
        # return the URL
        return url

    def mount_driver_from_bucket_name(self, bucket_name):
        for provider in settings.STORAGE_PROVIDERS:
            if settings.STORAGE_PROVIDERS[provider]["bucket"] == bucket_name:
                self.__init__(provider_name=provider)
                return True
        return False
