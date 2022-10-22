import logging
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.db.models import Q

import django_filters
import graphene
from graphene_django import DjangoObjectType

# models defination
from core.models import (
    BusinessDetailsAndCategoryGrouping,
    Category,
    FollowerFollowedMapping,
)

# get Nodes definitions
from core.schema.node import FollowerFollowedMappingFilter, FollowerFollowedMappingNode

# Get an instance of a logger
logger = logging.getLogger(__name__)

# class CreateOrUpdateFollowerFollowedMapping(graphene.relay.ClientIDMutation):
#     follower_followed_mapping = graphene.Field(FollowerFollowedMappingNode)

#     class Input:
#         followed = graphene.Int(required=True)
#         follow = graphene.Int(default=1)

#     def mutate_and_get_payload(root, info, **input):
#         user = info.context.user
#         followerFollowedMapping, _ = FollowerFollowedMapping.objects.update_or_create(
#             follower = user,
#             followed = get_user_model().objects.get(id=input.get('followed')),
#             defaults = {
#                 'follow': bool(int(input.get('follow')))
#             }
#         )
#         return CreateOrUpdateFollowerFollowedMapping(follower_followed_mapping=followerFollowedMapping)


class Mutation(graphene.AbstractType):
    # create_or_update_follower = CreateOrUpdateFollowerFollowedMapping.Field()
    pass
    # update_user = UpdateUser.Field()
