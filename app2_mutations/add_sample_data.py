"""
Script to populate the database with sample data for App 2.

Run this after migrations:
python manage.py shell < add_sample_data.py
"""

import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mutations_app.models import Author, Publisher, Book, Review

# Clear existing data
Review.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()
Publisher.objects.all().delete()

print("Creating publishers...")

# Create publishers
pub1 = Publisher.objects.create(
    name='Bloomsbury Publishing',
    country='United Kingdom',
    established_year=1986
)

pub2 = Publisher.objects.create(
    name='Bantam Books',
    country='United States',
    established_year=1945
)

pub3 = Publisher.objects.create(
    name='HarperCollins',
    country='United States',
    established_year=1989
)

print("Creating authors...")

# Create authors
author1 = Author.objects.create(
    name='J.K. Rowling',
    email='jk.rowling@example.com',
    bio='British author, best known for the Harry Potter series.',
    birth_year=1965
)
author1.publishers.add(pub1)

author2 = Author.objects.create(
    name='George R.R. Martin',
    email='george.martin@example.com',
    bio='American author, known for A Song of Ice and Fire series.',
    birth_year=1948
)
author2.publishers.add(pub2)

author3 = Author.objects.create(
    name='J.R.R. Tolkien',
    email='jrr.tolkien@example.com',
    bio='British author and philologist, created Middle Earth.',
    birth_year=1892
)
author3.publishers.add(pub3)

print("Creating books...")

# Create books
book1 = Book.objects.create(
    title='Harry Potter and the Philosopher Stone',
    description='A young wizard discovers the magical world and his own destiny.',
    author=author1,
    publisher=pub1,
    published_date=datetime(1997, 6, 26).date(),
    pages=309,
    isbn='978-0747532699'
)

book2 = Book.objects.create(
    title='Harry Potter and the Chamber of Secrets',
    description='Harry returns to Hogwarts and encounters a mysterious chamber.',
    author=author1,
    publisher=pub1,
    published_date=datetime(1998, 7, 2).date(),
    pages=341,
    isbn='978-0747538494'
)

book3 = Book.objects.create(
    title='A Game of Thrones',
    description='Complex political intrigue and fantastical battles in Westeros.',
    author=author2,
    publisher=pub2,
    published_date=datetime(1996, 8, 6).date(),
    pages=694,
    isbn='978-0553103540'
)

book4 = Book.objects.create(
    title='A Clash of Kings',
    description='War erupts across the Seven Kingdoms.',
    author=author2,
    publisher=pub2,
    published_date=datetime(1999, 11, 16).date(),
    pages=761,
    isbn='978-0553108033'
)

book5 = Book.objects.create(
    title='The Hobbit',
    description='An unexpected journey of a hobbit and a treasure.',
    author=author3,
    publisher=pub3,
    published_date=datetime(1937, 9, 21).date(),
    pages=310,
    isbn='978-0547928227'
)

print("Creating reviews...")

# Create reviews
review1 = Review.objects.create(
    book=book1,
    rating=5,
    review_text='An amazing start to the Harry Potter series. Highly recommended!',
    reviewer_name='Sarah Johnson'
)

review2 = Review.objects.create(
    book=book3,
    rating=4,
    review_text='A complex and engaging fantasy epic. A must-read for fantasy fans.',
    reviewer_name='Michael Chen'
)

review3 = Review.objects.create(
    book=book5,
    rating=5,
    review_text='A classic adventure tale that is both entertaining and thought-provoking.',
    reviewer_name='Emma Wilson'
)

print("✅ Sample data created successfully!")
print(f"Created {Publisher.objects.count()} publishers")
print(f"Created {Author.objects.count()} authors")
print(f"Created {Book.objects.count()} books")
print(f"Created {Review.objects.count()} reviews")
