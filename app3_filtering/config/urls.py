"""
URL configuration for app3_filtering project.
"""

from django.urls import path
from graphene_django.views import GraphQLView
from config.schema import schema

urlpatterns = [
    path('graphql/', GraphQLView.as_view(schema=schema)),
]
