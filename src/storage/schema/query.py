import graphene
from graphene_django.filter import DjangoFilterConnectionField

from storage.schema.node import ImageNode


class Query(graphene.ObjectType):
    pass
