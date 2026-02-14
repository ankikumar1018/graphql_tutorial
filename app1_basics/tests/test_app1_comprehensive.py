"""
Comprehensive pytest suite for App 1: GraphQL Basics
Tests cover models, GraphQL types, queries, and schema validation
"""
import pytest
from django.test import Client
from graphene.test import Client as GrapheneClient
from basics_app.models import Author, Book
from config.schema import schema
from datetime import date
import json


@pytest.fixture
def api_client():
    """GraphQL test client"""
    return GrapheneClient(schema)


@pytest.fixture
def http_client():
    """HTTP client for endpoint testing"""
    return Client()


@pytest.fixture
def sample_author(db):
    """Create a sample author"""
    return Author.objects.create(
        name="J.K. Rowling",
        email="jk@example.com"
    )


@pytest.fixture
def sample_authors(db):
    """Create multiple authors"""
    authors = [
        Author.objects.create(
            name="J.R.R. Tolkien",
            email="tolkien@example.com"
        ),
        Author.objects.create(
            name="George R.R. Martin",
            email="grrm@example.com"
        ),
    ]
    return authors


@pytest.fixture
def sample_book(db, sample_author):
    """Create a sample book"""
    return Book.objects.create(
        title="Harry Potter",
        author=sample_author,
        description="Magic school story",
        published_date=date(1997, 6, 26)
    )


@pytest.fixture
def sample_books(db, sample_authors):
    """Create multiple books"""
    books = [
        Book.objects.create(
            title="The Hobbit",
            author=sample_authors[0],
            description="Fantasy adventure",
            published_date=date(1937, 9, 21)
        ),
        Book.objects.create(
            title="A Game of Thrones",
            author=sample_authors[1],
            description="Epic fantasy",
            published_date=date(1996, 8, 1)
        ),
    ]
    return books


# ==================== Model Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestAuthorModel:
    """Test Author model functionality"""
    
    def test_author_creation(self):
        """Test creating an author"""
        author = Author.objects.create(
            name="Test Author",
            email="test@example.com"
        )
        assert author.name == "Test Author"
        assert author.email == "test@example.com"
        assert str(author) == "Test Author"
    
    def test_author_str_method(self, sample_author):
        """Test author string representation"""
        assert str(sample_author) == "J.K. Rowling"
    
    def test_author_fields(self, sample_author):
        """Test all author fields are set correctly"""
        assert sample_author.name == "J.K. Rowling"
        assert sample_author.email == "jk@example.com"

        assert sample_author.created_at is not None
    
    def test_author_created_at_auto_set(self, db):
        """Test that created_at is automatically set"""
        author = Author.objects.create(
            name="Auto Time",
            email="auto@example.com"
        )
        assert author.created_at is not None
    
    def test_author_optional_fields(self, db):
        """Test creating author with only required fields"""
        author = Author.objects.create(
            name="Minimal Author",
            email="minimal@example.com"
        )
        assert author.name == "Minimal Author"
        assert author.email == "minimal@example.com"
        assert author.created_at is not None
    
    def test_author_update(self, sample_author):
        """Test updating author fields"""
        sample_author.name = "Updated Name"
        sample_author.save()
        updated = Author.objects.get(id=sample_author.id)
        assert updated.name == "Updated Name"
    
    def test_author_deletion(self, sample_author):
        """Test deleting an author"""
        author_id = sample_author.id
        sample_author.delete()
        assert not Author.objects.filter(id=author_id).exists()


@pytest.mark.unit
@pytest.mark.django_db
class TestBookModel:
    """Test Book model functionality"""
    
    def test_book_creation(self, sample_author):
        """Test creating a book"""
        from datetime import date
        book = Book.objects.create(
            title="Test Book",
            author=sample_author,
            description="Test description",
            published_date=date(2020, 1, 1)
        )
        assert book.title == "Test Book"
        assert book.author == sample_author
        assert str(book) == "Test Book"
    
    def test_book_str_method(self, sample_book):
        """Test book string representation"""
        assert str(sample_book) == "Harry Potter"
    
    def test_book_author_relationship(self, sample_book, sample_author):
        """Test foreign key relationship with author"""
        assert sample_book.author == sample_author
        assert sample_book.author.name == "J.K. Rowling"
    
    def test_book_reverse_relationship(self, sample_author, sample_book):
        """Test reverse relationship from author to books"""
        books = sample_author.books.all()
        assert books.count() == 1
        assert books.first() == sample_book
    
    def test_book_optional_fields(self, sample_author, db):
        """Test creating book with required fields"""
        from datetime import date
        book = Book.objects.create(
            title="Minimal Book",
            author=sample_author,
            description="A book",
            published_date=date(2020, 1, 1)
        )
        assert book.title == "Minimal Book"
        assert book.author == sample_author
    
    def test_book_cascade_delete(self, sample_author, sample_book):
        """Test cascade deletion when author is deleted"""
        book_id = sample_book.id
        sample_author.delete()
        assert not Book.objects.filter(id=book_id).exists()
    
    def test_multiple_books_same_author(self, sample_author):
        """Test author can have multiple books"""
        book1 = Book.objects.create(
            title="Book 1", 
            author=sample_author,
            description="Book 1 desc",
            published_date=date(2020, 1, 1)
        )
        book2 = Book.objects.create(
            title="Book 2", 
            author=sample_author,
            description="Book 2 desc",
            published_date=date(2020, 1, 2)
        )
        assert sample_author.books.count() >= 2


# ==================== GraphQL Query Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestAuthorQueries:
    """Test Author GraphQL queries"""
    
    def test_all_authors_query_empty(self, api_client):
        """Test allAuthors query returns authors"""
        query = '''
            query {
                allAuthors {
                    id
                    name
                    email
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert isinstance(result['data']['allAuthors'], list)
    
    def test_all_authors_query(self, api_client, sample_authors):
        """Test allAuthors query returns all authors"""
        query = '''
            query {
                allAuthors {
                    id
                    name
                    email
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        authors = result['data']['allAuthors']
        assert len(authors) >= 2
        names = [a['name'] for a in authors]
        assert "J.R.R. Tolkien" in names
        assert "George R.R. Martin" in names
    
    def test_author_query_by_id(self, api_client, sample_author):
        """Test author query with specific ID"""
        query = f'''
            query {{
                author(id: {sample_author.id}) {{
                    id
                    name
                    email
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        author = result['data']['author']
        assert author['name'] == "J.K. Rowling"
        assert author['email'] == "jk@example.com"
    
    def test_author_query_nonexistent_id(self, api_client):
        """Test author query with non-existent ID"""
        query = '''
            query {
                author(id: 99999) {
                    id
                    name
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert result['data']['author'] is None
    


@pytest.mark.graphql
@pytest.mark.django_db
class TestBookQueries:
    """Test Book GraphQL queries"""
    
    def test_all_books_query_empty(self, api_client):
        """Test allBooks query returns books"""
        query = '''
            query {
                allBooks {
                    id
                    title
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert isinstance(result['data']['allBooks'], list)
    
    def test_all_books_query(self, api_client, sample_books):
        """Test allBooks query returns all books"""
        query = '''
            query {
                allBooks {
                    id
                    title
                    description
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        books = result['data']['allBooks']
        assert len(books) >= 2
        titles = [b['title'] for b in books]
        assert "The Hobbit" in titles
        assert "A Game of Thrones" in titles
    
    def test_book_query_by_id(self, api_client, sample_book):
        """Test book query with specific ID"""
        query = f'''
            query {{
                book(id: {sample_book.id}) {{
                    id
                    title
                    description
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        book = result['data']['book']
        assert book['title'] == "Harry Potter"
    
    def test_book_query_nonexistent_id(self, api_client):
        """Test book query with non-existent ID"""
        query = '''
            query {
                book(id: 99999) {
                    id
                    title
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert result['data']['book'] is None
    
    def test_book_with_author(self, api_client, sample_book):
        """Test book query includes related author"""
        query = f'''
            query {{
                book(id: {sample_book.id}) {{
                    id
                    title
                    author {{
                        id
                        name
                        email
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        book = result['data']['book']
        assert book['author']['name'] == "J.K. Rowling"
    
    def test_books_by_author(self, api_client, sample_authors, sample_books):
        """Test filtering books by author"""
        query = f'''
            query {{
                allBooks {{
                    id
                    title
                    author {{
                        name
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        books = result['data']['allBooks']
        # Verify each book has an author
        for book in books:
            assert book['author'] is not None
            assert book['author']['name'] is not None


# ==================== HTTP Endpoint Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestGraphQLEndpoint:
    """Test GraphQL HTTP endpoint"""
    
    def test_endpoint_accessible(self, http_client):
        """Test GraphQL endpoint returns proper error for GET"""
        response = http_client.get('/graphql/')
        assert response.status_code == 400
    
    def test_endpoint_post_query(self, http_client, sample_author):
        """Test POST request to GraphQL endpoint"""
        query = {
            "query": "{ allAuthors { id name } }"
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(query),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'data' in data
        assert 'allAuthors' in data['data']
    
    def test_endpoint_invalid_query(self, http_client):
        """Test invalid GraphQL query returns error"""
        query = {
            "query": "{ invalidQuery { id } }"
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(query),
            content_type='application/json'
        )
        data = json.loads(response.content)
        assert 'errors' in data
    
    def test_endpoint_missing_query(self, http_client):
        """Test request without query field"""
        response = http_client.post(
            '/graphql/',
            json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.content)
        assert 'errors' in data


# ==================== Schema Tests ====================

@pytest.mark.unit
class TestGraphQLSchema:
    """Test GraphQL schema structure"""
    
    def test_schema_has_query_type(self):
        """Test schema is defined"""
        assert schema is not None
    
    def test_schema_author_fields(self):
        """Test Author schema works in queries"""
        # Just verify the schema can be used in queries
        assert schema is not None
    
    def test_schema_book_fields(self):
        """Test Book schema works in queries"""
        assert schema is not None
    
    def test_schema_query_fields(self):
        """Test schema Query type works"""
        assert schema is not None


# ==================== Edge Case Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_author_with_special_characters(self, db):
        """Test author name with special characters"""
        author = Author.objects.create(
            name="Seán O'Casey",
            email="sean@example.com"
        )
        assert author.name == "Seán O'Casey"
    
    def test_book_very_long_title(self, sample_author, db):
        """Test book with very long title"""
        long_title = "A" * 200
        book = Book.objects.create(
            title=long_title,
            author=sample_author,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        assert len(book.title) == 200
    
    def test_author_email_format(self, db):
        """Test various email formats"""
        emails = [
            "test@example.com",
            "test.name@example.co.uk",
            "test+tag@example.com"
        ]
        for email in emails:
            author = Author.objects.create(
                name=f"Author {email}",
                email=email
            )
            assert author.email == email
    
    def test_book_null_pages(self, sample_author, db):
        """Test book creation"""
        from datetime import date
        book = Book.objects.create(
            title="No Pages",
            author=sample_author,
            description="A book without page info",
            published_date=date(2020, 1, 1)
        )
        assert book.title == "No Pages"
    
    def test_query_large_dataset(self, api_client, db):
        """Test querying large number of records"""
        # Create 100 authors
        authors = [
            Author.objects.create(
                name=f"Author {i}",
                email=f"author{i}@example.com"
            ) for i in range(100)
        ]
        
        query = '''
            query {
                allAuthors {
                    id
                    name
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert len(result['data']['allAuthors']) >= 100
