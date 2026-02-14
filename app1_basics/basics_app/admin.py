"""
Django Admin configuration for App 1.
Allows easy management of Author and Book models through Django admin.
"""

from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'created_at']
    search_fields = ['title', 'author__name']
    list_filter = ['published_date', 'author']
    raw_id_fields = ['author']
