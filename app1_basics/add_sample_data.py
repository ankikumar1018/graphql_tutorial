"""
Script to populate the database with sample data.

Run this after migrations:
python manage.py shell < add_sample_data.py
"""

import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from basics_app.models import Author, Book

# Clear existing data
Author.objects.all().delete()
Book.objects.all().delete()

# Create sample authors
author1 = Author.objects.create(
    name='J.K. Rowling',
    email='jk.rowling@example.com'
)

author2 = Author.objects.create(
    name='George R.R. Martin',
    email='george.martin@example.com'
)

author3 = Author.objects.create(
    name='J.R.R. Tolkien',
    email='jrr.tolkien@example.com'
)

# Create sample books
book1 = Book.objects.create(
    title='Harry Potter and the Philosopher Stone',
    description='A young wizard discovers the magical world and his own destiny.',
    author=author1,
    published_date=datetime(1997, 6, 26).date()
)

book2 = Book.objects.create(
    title='Harry Potter and the Chamber of Secrets',
    description='Harry returns to Hogwarts and encounters a mysterious chamber.',
    author=author1,
    published_date=datetime(1998, 7, 2).date()
)

book3 = Book.objects.create(
    title='A Game of Thrones',
    description='Complex political intrigue and fantastical battles in Westeros.',
    author=author2,
    published_date=datetime(1996, 8, 6).date()
)

book4 = Book.objects.create(
    title='A Clash of Kings',
    description='War erupts across the Seven Kingdoms.',
    author=author2,
    published_date=datetime(1999, 11, 16).date()
)

book5 = Book.objects.create(
    title='The Hobbit',
    description='An unexpected journey of a hobbit and a treasure.',
    author=author3,
    published_date=datetime(1937, 9, 21).date()
)

print("✅ Sample data created successfully!")
print(f"Created {Author.objects.count()} authors and {Book.objects.count()} books")
