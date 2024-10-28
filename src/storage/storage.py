from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage


class MultiStorage(Storage):
    """
    Base Storage class to abstract the storage function accross the multiple service providers
    """

    # hold the drive then main connection the provider
    driver = None
    # hold the provider data
    provider = settings.STORAGE_PROVIDERS["default"]
    # hold the bucket data
    bucket = None

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
