"""
Django Models for App 2: Mutations, Validation & Relationships

This module demonstrates:
- Model definition
- ForeignKey relationships
- OneToOne relationships
- ManyToMany relationships
- Field validation
"""

from django.db import models
from django.core.exceptions import ValidationError


class Publisher(models.Model):
    """
    Publisher model - represents a book publisher.
    
    Fields:
    - name: Publisher's name
    - country: Country of origin
    - established_year: Year the publisher was established
    """
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    established_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Author model - represents an author.
    
    Fields:
    - name: Author's full name
    - email: Author's email address (unique)
    - bio: Short biography
    - birth_year: Author's birth year
    - publishers: ManyToMany relationship with Publisher
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    publishers = models.ManyToManyField(Publisher, related_name='authors', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def clean(self):
        """Validate author data."""
        if self.birth_year and self.birth_year > 2024:
            raise ValidationError({'birth_year': 'Birth year cannot be in the future.'})


class Book(models.Model):
    """
    Book model - represents a book with relationships.
    
    Fields:
    - title: Book title
    - description: Book description
    - author: ForeignKey to Author (one author can have many books)
    - publisher: ForeignKey to Publisher
    - published_date: When the book was published
    - pages: Number of pages
    - isbn: ISBN number (unique, optional)
    """
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    published_date = models.DateField()
    pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        """Validate book data."""
        if self.pages and self.pages <= 0:
            raise ValidationError({'pages': 'Number of pages must be greater than 0.'})


class Review(models.Model):
    """
    Review model - OneToOne relationship example.
    
    Fields:
    - book: OneToOne relationship with Book
    - rating: Rating from 1-5
    - review_text: Review content
    - reviewer_name: Name of the reviewer
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    reviewer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.book.title}"

    def clean(self):
        """Validate review data."""
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})
