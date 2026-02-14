from django.urls import path
from django.views.decorators.http import csrf_exempt
from graphene_django.views import GraphQLView
from config.schema import schema

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema))),
]
