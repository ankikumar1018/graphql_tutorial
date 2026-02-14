"""
Tests for App 1 GraphQL queries.

Run tests with:
python manage.py test basics_app.tests
"""

from django.test import TestCase, Client
from basics_app.models import Author, Book
from datetime import datetime
import json


class AuthorModelTests(TestCase):
    """Test Author model."""

    def setUp(self):
        Author.objects.create(
            name='Test Author',
            email='test@example.com'
        )

    def test_author_creation(self):
        author = Author.objects.get(name='Test Author')
        self.assertEqual(author.email, 'test@example.com')

    def test_author_str(self):
        author = Author.objects.get(name='Test Author')
        self.assertEqual(str(author), 'Test Author')


class BookModelTests(TestCase):
    """Test Book model."""

    def setUp(self):
        self.author = Author.objects.create(
            name='Test Author',
            email='test@example.com'
        )
        Book.objects.create(
            title='Test Book',
            description='Test Description',
            author=self.author,
            published_date=datetime(2020, 1, 1).date()
        )

    def test_book_creation(self):
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.author.name, 'Test Author')
        self.assertEqual(book.description, 'Test Description')

    def test_book_str(self):
        book = Book.objects.get(title='Test Book')
        self.assertEqual(str(book), 'Test Book')


class GraphQLQueryTests(TestCase):
    """Test GraphQL queries."""

    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(
            name='J.K. Rowling',
            email='jk@example.com'
        )
        self.book = Book.objects.create(
            title='Harry Potter',
            description='A young wizard',
            author=self.author,
            published_date=datetime(1997, 6, 26).date()
        )

    def test_all_authors_query(self):
        query = '''
        {
            allAuthors {
                id
                name
                email
            }
        }
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_author_by_id_query(self):
        query = f'''
        {{
            author(id: {self.author.id}) {{
                id
                name
                email
            }}
        }}
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_all_books_query(self):
        query = '''
        {
            allBooks {
                id
                title
                author {
                    name
                }
            }
        }
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_book_by_id_query(self):
        query = f'''
        {{
            book(id: {self.book.id}) {{
                id
                title
                author {{
                    name
                }}
            }}
        }}
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
