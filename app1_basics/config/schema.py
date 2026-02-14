"""
GraphQL Schema definition for App 1: GraphQL Basics & Django Models

This module demonstrates:
- ObjectType definition
- Query definition
- Fetching single objects
- Fetching lists of objects
- Resolvers
"""

import graphene
from graphene_django import DjangoObjectType
from basics_app.models import Author, Book


# Define ObjectTypes - these convert Django models to GraphQL types
class AuthorType(DjangoObjectType):
    """
    GraphQL type for Author model.
    Automatically includes all fields from the Author model.
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'created_at']


class BookType(DjangoObjectType):
    """
    GraphQL type for Book model.
    This includes nested author data.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'published_date', 'created_at']


# Define the Root Query - entry point for all queries
class Query(graphene.ObjectType):
    """
    Root Query type - defines all available queries in the API.
    """

    # Query to get all authors
    all_authors = graphene.List(AuthorType, description="Get all authors")
    
    # Query to get single author by ID
    author = graphene.Field(AuthorType, id=graphene.Int(required=True), description="Get author by ID")
    
    # Query to get all books
    all_books = graphene.List(BookType, description="Get all books")
    
    # Query to get single book by ID
    book = graphene.Field(BookType, id=graphene.Int(required=True), description="Get book by ID")

    # Resolver for all_authors query
    def resolve_all_authors(self, info):
        """
        Fetches all authors from the database.
        
        Example Query:
        {
            allAuthors {
                id
                name
                email
                createdAt
            }
        }
        """
        return Author.objects.all()

    # Resolver for author query
    def resolve_author(self, info, id):
        """
        Fetches a single author by ID.
        
        Example Query:
        {
            author(id: 1) {
                id
                name
                email
            }
        }
        """
        try:
            return Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return None

    # Resolver for all_books query
    def resolve_all_books(self, info):
        """
        Fetches all books from the database.
        
        Example Query:
        {
            allBooks {
                id
                title
                description
                author {
                    id
                    name
                }
                publishedDate
            }
        }
        """
        return Book.objects.select_related('author').all()

    # Resolver for book query
    def resolve_book(self, info, id):
        """
        Fetches a single book by ID.
        
        Example Query:
        {
            book(id: 1) {
                id
                title
                description
                author {
                    id
                    name
                    email
                }
            }
        }
        """
        try:
            return Book.objects.select_related('author').get(pk=id)
        except Book.DoesNotExist:
            return None


# Create the schema
schema = graphene.Schema(query=Query)
