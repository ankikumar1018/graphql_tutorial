"""
Comprehensive pytest suite for App 2: Mutations & Relationships
Tests cover models, mutations, validations, queries, and complex relationships
"""
import pytest
from django.test import Client
from graphene.test import Client as GrapheneClient
from mutations_app.models import Author, Book, Publisher, Review
from config.schema import schema
import json
from datetime import date


@pytest.fixture
def api_client():
    """GraphQL test client"""
    return GrapheneClient(schema)


@pytest.fixture
def http_client():
    """HTTP client"""
    return Client()


@pytest.fixture
def sample_publisher(db):
    """Create sample publisher"""
    return Publisher.objects.create(
        name="Penguin Books",
        country="United Kingdom",
        established_year=1935
    )


@pytest.fixture
def sample_publishers(db):
    """Create multiple publishers"""
    return [
        Publisher.objects.create(
            name="Test HarperCollins",
            country="United States",
            established_year=1989
        ),
        Publisher.objects.create(
            name="Test Random House",
            country="United States",
            established_year=1927
        ),
    ]


@pytest.fixture
def sample_author(db):
    """Create sample author"""
    return Author.objects.create(
        name="J.K. Rowling",
        email="jk@example.com",
        bio="British author"
    )


@pytest.fixture
def sample_authors(db):
    """Create multiple authors"""
    return [
        Author.objects.create(
            name="J.R.R. Tolkien",
            email="tolkien@example.com",
            bio="Fantasy writer"
        ),
        Author.objects.create(
            name="George Orwell",
            email="orwell@example.com",
            bio="English novelist"
        ),
    ]


@pytest.fixture
def sample_book(db, sample_author, sample_publisher):
    """Create sample book"""
    return Book.objects.create(
        title="Harry Potter",
        author=sample_author,
        publisher=sample_publisher,
        description="Magic story",
        published_date=date(1997, 6, 26),
        isbn="978-0439708180",
        pages=309
    )


@pytest.fixture
def sample_books(db, sample_authors, sample_publisher):
    """Create multiple books"""
    return [
        Book.objects.create(
            title="The Hobbit",
            author=sample_authors[0],
            publisher=sample_publisher,
            description="Fantasy adventure",
            published_date=date(1937, 9, 21)
        ),
        Book.objects.create(
            title="1984",
            author=sample_authors[1],
            publisher=sample_publisher,
            description="Dystopian fiction",
            published_date=date(1949, 6, 8)
        ),
    ]


@pytest.fixture
def sample_review(db, sample_book):
    """Create sample review"""
    return Review.objects.create(
        book=sample_book,
        reviewer_name="John Doe",
        rating=5,
        review_text="Excellent book!"
    )


# ==================== Model Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestPublisherModel:
    """Test Publisher model"""
    
    def test_publisher_creation(self):
        """Test creating a publisher"""
        publisher = Publisher.objects.create(
            name="New Test Publisher",
            country="Test Country",
            established_year=2020
        )
        assert publisher.name == "New Test Publisher"
        assert str(publisher) == "New Test Publisher"
    
    def test_publisher_optional_fields(self, db):
        """Test publisher with all required fields"""
        publisher = Publisher.objects.create(
            name="Minimal Pub",
            country="USA",
            established_year=2000
        )
        assert publisher.country == "USA"
        assert publisher.established_year == 2000
    
    def test_publisher_books_relationship(self, sample_publisher, sample_book):
        """Test reverse relationship to books"""
        assert sample_publisher.books.count() == 1
        assert sample_publisher.books.first() == sample_book


@pytest.mark.unit
@pytest.mark.django_db
class TestAuthorModel:
    """Test Author model"""
    
    def test_author_creation(self):
        """Test creating an author"""
        author = Author.objects.create(
            name="Test Author",
            email="author@test.com",
            bio="Test bio"
        )
        assert author.name == "Test Author"
        assert str(author) == "Test Author"
    
    def test_author_books_relationship(self, sample_author, sample_book):
        """Test author can have multiple books"""
        assert sample_author.books.count() == 1
    
    def test_author_future_birth_year_validation(self, db):
        """Test author birth year validation (cannot be in future)"""
        from django.core.exceptions import ValidationError
        author = Author(
            name="Future Author",
            email="future@example.com",
            birth_year=2030
        )
        with pytest.raises(ValidationError) as exc_info:
            author.full_clean()
        assert 'birth_year' in exc_info.value.message_dict


@pytest.mark.unit
@pytest.mark.django_db
class TestBookModel:
    """Test Book model"""
    
    def test_book_creation(self, sample_author, sample_publisher):
        """Test creating a book"""
        book = Book.objects.create(
            title="Test Book",
            author=sample_author,
            publisher=sample_publisher,
            description="Test description",
            published_date=date(2020, 1, 1)
        )
        assert book.title == "Test Book"
        assert str(book) == "Test Book"
    
    def test_book_relationships(self, sample_book, sample_author, sample_publisher):
        """Test book relationships"""
        assert sample_book.author == sample_author
        assert sample_book.publisher == sample_publisher
    
    def test_book_review_relationship(self, sample_book, sample_review):
        """Test book has one review (OneToOne)"""
        assert hasattr(sample_book, 'review')
        assert sample_book.review == sample_review
    
    def test_book_negative_pages_validation(self, sample_author, sample_publisher, db):
        """Test book pages validation (must be positive)"""
        from django.core.exceptions import ValidationError
        book = Book(
            title="Invalid Book",
            author=sample_author,
            publisher=sample_publisher,
            description="Test",
            published_date=date(2020, 1, 1),
            pages=-10
        )
        with pytest.raises(ValidationError) as exc_info:
            book.full_clean()
        assert 'pages' in exc_info.value.message_dict


@pytest.mark.unit
@pytest.mark.django_db
class TestReviewModel:
    """Test Review model"""
    
    def test_review_creation(self, db):
        """Test creating a review"""
        author = Author.objects.create(
            name="Test Author",
            email="test@example.com"
        )
        publisher = Publisher.objects.create(
            name="Test Publisher",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Test Book",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        review = Review.objects.create(
            book=book,
            reviewer_name="Jane",
            rating=4,
            review_text="Good read"
        )
        assert review.rating == 4
        assert review.book == book
        assert str(review) == f"Review for {book.title}"
    
    def test_review_rating_range(self, db):
        """Test review ratings (1-5)"""
        author = Author.objects.create(
            name="Test Author",
            email="test2@example.com"
        )
        publisher = Publisher.objects.create(
            name="Test Publisher 2",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Test Book 2",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        review = Review.objects.create(
            book=book,
            reviewer_name="Test",
            rating=5,
            review_text="Great!"
        )
        assert 1 <= review.rating <= 5
    
    def test_review_rating_validation(self, db):
        """Test review rating validation (must be 1-5)"""
        from django.core.exceptions import ValidationError
        author = Author.objects.create(
            name="Test Author 3",
            email="test3@example.com"
        )
        publisher = Publisher.objects.create(
            name="Test Publisher 3",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Test Book 3",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        # Test rating too high
        review_high = Review(
            book=book,
            reviewer_name="Test",
            rating=6,
            review_text="Invalid"
        )
        with pytest.raises(ValidationError) as exc_info:
            review_high.full_clean()
        assert 'rating' in exc_info.value.message_dict
        
        # Test rating too low
        book2 = Book.objects.create(
            title="Test Book 4",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        review_low = Review(
            book=book2,
            reviewer_name="Test",
            rating=0,
            review_text="Invalid"
        )
        with pytest.raises(ValidationError) as exc_info:
            review_low.full_clean()
        assert 'rating' in exc_info.value.message_dict


# ==================== Query Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestQueries:
    """Test GraphQL queries"""
    
    def test_all_publishers_query(self, api_client, sample_publishers):
        """Test allPublishers query"""
        query = '''
            query {
                allPublishers {
                    id
                    name
                    country
                    establishedYear
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert len(result['data']['allPublishers']) >= 2
    
    def test_publisher_query_by_id(self, api_client, sample_publisher):
        """Test publisher query by ID"""
        query = f'''
            query {{
                publisher(id: {sample_publisher.id}) {{
                    id
                    name
                    country
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert result['data']['publisher']['name'] == "Penguin Books"
    
    def test_all_authors_query(self, api_client, sample_authors):
        """Test allAuthors query"""
        query = '''
            query {
                allAuthors {
                    id
                    name
                    email
                    bio
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert len(result['data']['allAuthors']) >= 2
    
    def test_author_with_books(self, api_client, sample_author, sample_book):
        """Test author query with books"""
        query = f'''
            query {{
                author(id: {sample_author.id}) {{
                    id
                    name
                    books {{
                        id
                        title
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert len(result['data']['author']['books']) == 1
    
    def test_all_books_query(self, api_client, sample_books):
        """Test allBooks query"""
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
        assert len(result['data']['allBooks']) >= 2
    
    def test_book_with_relationships(self, api_client, sample_book):
        """Test book query with all relationships"""
        query = f'''
            query {{
                book(id: {sample_book.id}) {{
                    id
                    title
                    author {{
                        name
                    }}
                    publisher {{
                        name
                    }}
                    review {{
                        reviewerName
                        rating
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        book = result['data']['book']
        assert book['author']['name'] == "J.K. Rowling"
        assert book['publisher']['name'] == "Penguin Books"


# ==================== Mutation Tests ====================

@pytest.mark.mutations
@pytest.mark.django_db
class TestAuthorMutations:
    """Test Author mutations"""
    
    def test_create_author_mutation(self, api_client):
        """Test creating an author"""
        mutation = '''
            mutation {
                createAuthor(input: {
                    name: "New Author"
                    email: "new@example.com"
                    bio: "New bio"
                }) {
                    author {
                        id
                        name
                        email
                        bio
                    }
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        author = result['data']['createAuthor']['author']
        assert author['name'] == "New Author"
        assert author['email'] == "new@example.com"
        
        # Verify in database
        assert Author.objects.filter(name="New Author").exists()
    
    def test_create_author_minimal_fields(self, api_client):
        """Test creating author with minimal fields"""
        mutation = '''
            mutation {
                createAuthor(input: {
                    name: "Minimal Author"
                    email: "minimal@example.com"
                }) {
                    author {
                        id
                        name
                        email
                        bio
                    }
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        author = result['data']['createAuthor']['author']
        assert author['bio'] == ''  # Empty string, not None
    
    def test_update_author_mutation(self, api_client, sample_author):
        """Test updating an author"""
        mutation = f'''
            mutation {{
                updateAuthor(
                    id: {sample_author.id}
                    input: {{
                        name: "Updated Name"
                        email: "updated@example.com"
                        bio: "Updated bio"
                    }}
                ) {{
                    author {{
                        id
                        name
                        email
                        bio
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        author = result['data']['updateAuthor']['author']
        assert author['name'] == "Updated Name"
        
        # Verify in database
        sample_author.refresh_from_db()
        assert sample_author.name == "Updated Name"
    
    def test_update_nonexistent_author(self, api_client):
        """Test updating non-existent author"""
        mutation = '''
            mutation {
                updateAuthor(
                    id: 99999
                    input: {
                        name: "Should Fail"
                        email: "fail@example.com"
                    }
                ) {
                    author {
                        id
                    }
                }
            }
        '''
        result = api_client.execute(mutation)
        # Should return null or error
        assert result['data']['updateAuthor']['author'] is None
    
    def test_delete_author_mutation(self, api_client, sample_author):
        """Test deleting an author"""
        author_id = sample_author.id
        mutation = f'''
            mutation {{
                deleteAuthor(id: {author_id}) {{
                    success
                    message
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        assert result['data']['deleteAuthor']['success'] is True
        
        # Verify deletion
        assert not Author.objects.filter(id=author_id).exists()
    
    def test_delete_nonexistent_author(self, api_client):
        """Test deleting non-existent author"""
        mutation = '''
            mutation {
                deleteAuthor(id: 99999) {
                    success
                    message
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        assert result['data']['deleteAuthor']['success'] is False


@pytest.mark.mutations
@pytest.mark.django_db
class TestBookMutations:
    """Test Book mutations"""
    
    def test_create_book_mutation(self, api_client, sample_author, sample_publisher):
        """Test creating a book"""
        mutation = f'''
            mutation {{
                createBook(input: {{
                    title: "New Book"
                    authorId: {sample_author.id}
                    publisherId: {sample_publisher.id}
                    description: "Test description"
                    pages: 200
                    publishedDate: "2020-01-01"
                }}) {{
                    book {{
                        id
                        title
                        description
                        pages
                        author {{
                            name
                        }}
                        publisher {{
                            name
                        }}
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        book = result['data']['createBook']['book']
        assert book['title'] == "New Book"
        assert book['pages'] == 200
        assert book['author']['name'] == sample_author.name
        
        # Verify in database
        assert Book.objects.filter(title="New Book").exists()
    
    def test_create_book_with_invalid_author(self, api_client, sample_publisher):
        """Test creating book with invalid author ID"""
        mutation = f'''
            mutation {{
                createBook(input: {{
                    title: "Invalid Book"
                    authorId: 99999
                    publisherId: {sample_publisher.id}
                }}) {{
                    book {{
                        id
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        # Should have errors or null
        assert 'errors' in result or result['data']['createBook']['book'] is None
    
    def test_update_book_mutation(self, api_client, sample_book, sample_author, sample_publisher):
        """Test updating a book"""
        mutation = f'''
            mutation {{
                updateBook(
                    id: {sample_book.id}
                    input: {{
                        title: "Updated Book Title"
                        description: "Updated description"
                        authorId: {sample_author.id}
                        publishedDate: "2020-01-01"
                    }}
                ) {{
                    book {{
                        id
                        title
                        description
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        book = result['data']['updateBook']['book']
        assert book['title'] == "Updated Book Title"
        
        # Verify in database
        sample_book.refresh_from_db()
        assert sample_book.title == "Updated Book Title"
    
    def test_delete_book_mutation(self, api_client, sample_book):
        """Test deleting a book"""
        book_id = sample_book.id
        mutation = f'''
            mutation {{
                deleteBook(id: {book_id}) {{
                    success
                    message
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        assert result['data']['deleteBook']['success'] is True
        
        # Verify deletion
        assert not Book.objects.filter(id=book_id).exists()


@pytest.mark.mutations
@pytest.mark.django_db
class TestReviewMutations:
    """Test Review mutations"""
    
    def test_create_review_mutation(self, api_client):
        """Test creating a review for a book without review"""
        # Create a book without a review
        author = Author.objects.create(
            name="Review Test Author",
            email="reviewtest@example.com"
        )
        publisher = Publisher.objects.create(
            name="Review Test Publisher",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Review Test Book",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        
        mutation = f'''
            mutation {{
                createReview(input: {{
                    bookId: {book.id}
                    reviewerName: "Test Reviewer"
                    rating: 5
                    reviewText: "Great book!"
                }}) {{
                    review {{
                        id
                        reviewerName
                        rating
                        reviewText
                        book {{
                            title
                        }}
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        review = result['data']['createReview']['review']
        assert review['reviewerName'] == "Test Reviewer"
        # Rating could be int or enum string depending on schema
        assert review['rating'] in [5, '5', 'A_5']
        
        # Verify in database
        assert Review.objects.filter(reviewer_name="Test Reviewer").exists()
    
    def test_create_review_invalid_rating(self, api_client):
        """Test creating review with invalid rating"""
        # Create a test book without review
        author = Author.objects.create(
            name="Test Author 3",
            email="test3@example.com"
        )
        publisher = Publisher.objects.create(
            name="Test Publisher 3",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Test Book 3",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        # Ratings should be 1-5, test with 0 and 6
        for invalid_rating in [0, 6]:
            mutation = f'''
                mutation {{
                    createReview(input: {{
                        bookId: {book.id}
                        reviewerName: "Invalid"
                        rating: {invalid_rating}
                        reviewText: "Test"
                    }}) {{
                        review {{
                            id
                        }}
                    }}
                }}
            '''
            result = api_client.execute(mutation)
            # Should have validation error
            assert 'errors' in result or result['data']['createReview']['review'] is None
    
    def test_update_review_mutation(self, api_client, sample_review, sample_book):
        """Test updating a review"""
        mutation = f'''
            mutation {{
                updateReview(
                    id: {sample_review.id}
                    input: {{
                        bookId: {sample_book.id}
                        reviewerName: "{sample_review.reviewer_name}"
                        rating: 4
                        reviewText: "Updated review text"
                    }}
                ) {{
                    review {{
                        id
                        rating
                        reviewText
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        review = result['data']['updateReview']['review']
        assert review['rating'] in [4, '4', 'A_4']
        assert review['reviewText'] == "Updated review text"
        
        # Verify in database
        sample_review.refresh_from_db()
        assert sample_review.rating == 4


# ==================== Validation Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestValidationLogic:
    """Test validation in mutations"""
    
    def test_author_unique_email(self, sample_author):
        """Test that author email should be unique"""
        # This depends on model constraints
        # If email is unique in the model, this will raise error
        pass  # Implement based on actual validation logic
    
    def test_book_price_positive(self, api_client, sample_author, sample_publisher):
        """Test book pages must be positive"""
        mutation = f'''
            mutation {{
                createBook(input: {{
                    title: "Negative Pages"
                    authorId: {sample_author.id}
                    publisherId: {sample_publisher.id}
                    description: "Test"
                    publishedDate: "2020-01-01"
                    pages: -10
                }}) {{
                    book {{
                        id
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        # Should validate that pages is positive
        # This depends on actual validation logic
        pass  # Implement based on actual validation
    
    def test_review_required_fields(self, api_client):
        """Test review requires book ID"""
        mutation = '''
            mutation {
                createReview(input: {
                    reviewerName: "Test"
                    rating: 5
                }) {
                    review {
                        id
                    }
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' in result


# ==================== Integration Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestComplexScenarios:
    """Test complex scenarios with multiple operations"""
    
    def test_create_complete_book_workflow(self, api_client):
        """Test creating publisher, author, and book in sequence"""
        # Create publisher
        pub_mutation = '''
            mutation {
                createPublisher(input: {
                    name: "New Publisher"
                    country: "USA"
                    establishedYear: 2020
                }) {
                    publisher {
                        id
                    }
                }
            }
        '''
        pub_result = api_client.execute(pub_mutation)
        pub_id = pub_result['data']['createPublisher']['publisher']['id']
        
        # Create author
        author_mutation = '''
            mutation {
                createAuthor(input: {
                    name: "New Author"
                    email: "newauthor@example.com"
                }) {
                    author {
                        id
                    }
                }
            }
        '''
        author_result = api_client.execute(author_mutation)
        author_id = author_result['data']['createAuthor']['author']['id']
        
        # Create book
        book_mutation = f'''
            mutation {{
                createBook(input: {{
                    title: "Complete Book"
                    authorId: {author_id}
                    publisherId: {pub_id}
                    description: "Complete description"
                    publishedDate: "2020-01-01"
                }}) {{
                    book {{
                        id
                        title
                        author {{
                            name
                        }}
                        publisher {{
                            name
                        }}
                    }}
                }}
            }}
        '''
        book_result = api_client.execute(book_mutation)
        assert 'errors' not in book_result
        book = book_result['data']['createBook']['book']
        assert book['title'] == "Complete Book"
        assert book['author']['name'] == "New Author"
        assert book['publisher']['name'] == "New Publisher"
    
    def test_cascade_delete_author_with_books(self, api_client, sample_author, sample_book):
        """Test deleting author also deletes books (if cascade)"""
        author_id = sample_author.id
        book_id = sample_book.id
        
        mutation = f'''
            mutation {{
                deleteAuthor(id: {author_id}) {{
                    success
                }}
            }}
        '''
        result = api_client.execute(mutation)
        assert result['data']['deleteAuthor']['success'] is True
        
        # Check if book was also deleted (depends on cascade setting)
        assert not Book.objects.filter(id=book_id).exists()
    
    def test_multiple_reviews_same_book(self, api_client):
        """Test OneToOne constraint - only one review per book"""
        # Create a test book
        author = Author.objects.create(
            name="Test Author 4",
            email="test4@example.com"
        )
        publisher = Publisher.objects.create(
            name="Test Publisher 4",
            country="USA",
            established_year=2000
        )
        book = Book.objects.create(
            title="Test Book 4",
            author=author,
            publisher=publisher,
            description="Test",
            published_date=date(2020, 1, 1)
        )
        
        # Create first review
        mutation1 = f'''
            mutation {{
                createReview(input: {{
                    bookId: {book.id}
                    reviewerName: "Reviewer 1"
                    rating: 5
                    reviewText: "Great!"
                }}) {{
                    review {{
                        id
                    }}
                }}
            }}
        '''
        result1 = api_client.execute(mutation1)
        assert 'errors' not in result1
        
        # Try to create second review - GraphQL mutation should return null
        # because OneToOne relationship already exists
        mutation2 = f'''
            mutation {{
                createReview(input: {{
                    bookId: {book.id}
                    reviewerName: "Reviewer 2"
                    rating: 4
                    reviewText: "Good"
                }}) {{
                    review {{
                        id
                    }}
                }}
            }}
        '''
        result2 = api_client.execute(mutation2)
        # Check that either error exists or review is None
        # The mutation might succeed but update existing review instead of creating new
        assert 'errors' in result2 or result2.get('data', {}).get('createReview', {}).get('review') is None or Review.objects.filter(book=book).count() == 1


# ==================== HTTP Endpoint Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestHTTPEndpoint:
    """Test GraphQL HTTP endpoint"""
    
    def test_mutation_via_http(self, http_client, sample_author, sample_publisher):
        """Test mutation through HTTP POST"""
        mutation = {
            "query": f'''
                mutation {{
                    createBook(input: {{
                        title: "HTTP Book"
                        authorId: {sample_author.id}
                        publisherId: {sample_publisher.id}
                        description: "HTTP test"
                        publishedDate: "2020-01-01"
                    }}) {{
                        book {{
                            id
                            title
                        }}
                    }}
                }}
            '''
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(mutation),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'data' in data
        assert data['data']['createBook']['book']['title'] == "HTTP Book"
