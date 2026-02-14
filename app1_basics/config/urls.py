"""
URL configuration for app1_basics project.
The graphql_view is configured here to handle GraphQL requests.
"""

from django.urls import path
from graphene_django.views import GraphQLView
from config.schema import schema

urlpatterns = [
    # GraphQL endpoint at /graphql/
    path('graphql/', GraphQLView.as_view(schema=schema)),
]
