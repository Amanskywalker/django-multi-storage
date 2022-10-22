import json
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field

from storage.models import (
    FileStorage,
    FileTransactionLogs
)

from storage.helper import (
    Storage
)

# File Node
class FileNode(graphene.Interface):
    '''
        Defines the custom file node

        it accepts the file id to view the file and its related details
    '''
    id = graphene.ID(required=True)
    url = graphene.String()

    def resolve_id(self, info):
        return self.hashed_name
    
    def resolve_url(self, info):
        storage = Storage()
        return storage.get_object_url(object_id=self.id)

# Image node
class ImageNode(graphene.ObjectType):
    '''
        Defines the custom Image node, it extends the File Node

        it accepts the file id to view the Image and its related details
    '''
    class Meta:
        interfaces = (graphene.relay.Node, FileNode)
    
    url_200 = graphene.String()
    def resolve_url_200(self, info):
        '''
            url of the 200 byte implimation of the image
        '''
        return "URL comming soon"

# Video node
class VideoNode(graphene.ObjectType):
    '''
        Defines the custom Video node, it extends the File Node

        it accepts the file id to view the Video and its related details
    '''
    class Meta:
        interfaces = (graphene.relay.Node, FileNode)
    
    stream_url = graphene.String()
    def resolve_stream_url(self, info):
        '''
            Streaming Url
        '''
        return "URL comming soon"
