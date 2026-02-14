"""
Django Admin configuration for App 2.
"""

from django.contrib import admin
from .models import Author, Publisher, Book, Review


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'established_year']
    search_fields = ['name']
    list_filter = ['established_year']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'birth_year', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at', 'publishers']
    filter_horizontal = ['publishers']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'published_date', 'pages']
    search_fields = ['title', 'author__name', 'isbn']
    list_filter = ['published_date', 'author', 'publisher']
    raw_id_fields = ['author', 'publisher']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'rating', 'reviewer_name', 'created_at']
    search_fields = ['book__title', 'reviewer_name']
    list_filter = ['rating', 'created_at']
