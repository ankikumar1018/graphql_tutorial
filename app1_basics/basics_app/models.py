"""
Django Models for App 1: GraphQL Basics & Django Models

This module demonstrates:
- Model definition
- Field types
- Relationships (ForeignKey)
- String representations
"""

from django.db import models


class Author(models.Model):
    """
    Author model - represents an author in the system.
    
    Fields:
    - name: Author's full name
    - email: Author's email address
    - created_at: Timestamp when author was created
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model - represents a book in the system.
    
    Fields:
    - title: Book title
    - description: Book description
    - author: ForeignKey to Author (one author can have many books)
    - published_date: When the book was published
    - created_at: Timestamp when book was added to system
    """
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
