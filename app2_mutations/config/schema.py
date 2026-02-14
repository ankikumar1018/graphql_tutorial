"""
GraphQL Schema definition for App 2: Mutations, Validation & Relationships

This module demonstrates:
- ObjectType definition
- Mutation definition (Create, Update, Delete)
- Input types for mutations
- Error handling and validation
- ForeignKey, OneToOne, ManyToMany relationships
- Nested queries with relationships
"""

import graphene
from graphene_django import DjangoObjectType
from graphene import InputObjectType, String, Int
from mutations_app.models import Author, Book, Publisher, Review
from django.core.exceptions import ValidationError


# =====================================================================
# GraphQL ObjectTypes - Convert Django models to GraphQL types
# =====================================================================

class PublisherType(DjangoObjectType):
    """GraphQL type for Publisher model."""
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'established_year', 'created_at']


class AuthorType(DjangoObjectType):
    """GraphQL type for Author model with relationships."""
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'birth_year', 'publishers', 'books', 'created_at']


class BookType(DjangoObjectType):
    """GraphQL type for Book model with relationships."""
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'publisher', 'published_date', 'pages', 'isbn', 'review', 'created_at']


class ReviewType(DjangoObjectType):
    """GraphQL type for Review model."""
    class Meta:
        model = Review
        fields = ['id', 'book', 'rating', 'review_text', 'reviewer_name', 'created_at']


# =====================================================================
# Input Types for Mutations
# =====================================================================

class AuthorInput(InputObjectType):
    """Input type for creating/updating authors."""
    name = String(required=True, description="Author's full name")
    email = String(required=True, description="Author's email (must be unique)")
    bio = String(description="Author's biography")
    birth_year = Int(description="Author's birth year")


class PublisherInput(InputObjectType):
    """Input type for creating/updating publishers."""
    name = String(required=True, description="Publisher's name")
    country = String(required=True, description="Publisher's country")
    established_year = Int(required=True, description="Year established")


class BookInput(InputObjectType):
    """Input type for creating/updating books."""
    title = String(required=True, description="Book title")
    description = String(required=True, description="Book description")
    author_id = Int(required=True, description="Author ID")
    publisher_id = Int(description="Publisher ID")
    published_date = String(required=True, description="Published date (YYYY-MM-DD)")
    pages = Int(description="Number of pages")
    isbn = String(description="ISBN number")


class ReviewInput(InputObjectType):
    """Input type for creating/updating reviews."""
    book_id = Int(required=True, description="Book ID")
    rating = Int(required=True, description="Rating 1-5")
    review_text = String(required=True, description="Review content")
    reviewer_name = String(required=True, description="Reviewer's name")


# =====================================================================
# Mutation Classes
# =====================================================================

class CreateAuthor(graphene.Mutation):
    """Create a new author."""
    
    class Arguments:
        input = AuthorInput(required=True)
    
    author = graphene.Field(AuthorType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        try:
            # Validate data
            if Author.objects.filter(email=input.email).exists():
                return CreateAuthor(success=False, message="Email already exists", author=None)
            
            author = Author.objects.create(
                name=input.name,
                email=input.email,
                bio=input.bio or "",
                birth_year=input.birth_year
            )
            author.full_clean()  # Run model validations
            author.save()
            
            return CreateAuthor(success=True, message="Author created successfully", author=author)
        except ValidationError as e:
            return CreateAuthor(success=False, message=str(e), author=None)
        except Exception as e:
            return CreateAuthor(success=False, message=f"Error: {str(e)}", author=None)


class UpdateAuthor(graphene.Mutation):
    """Update an existing author."""
    
    class Arguments:
        id = Int(required=True)
        input = AuthorInput(required=True)
    
    author = graphene.Field(AuthorType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id, input):
        try:
            author = Author.objects.get(pk=id)
            
            # Check if new email already exists (and is different from current)
            if input.email != author.email and Author.objects.filter(email=input.email).exists():
                return UpdateAuthor(success=False, message="Email already exists", author=None)
            
            author.name = input.name
            author.email = input.email
            if input.bio:
                author.bio = input.bio
            if input.birth_year:
                author.birth_year = input.birth_year
            
            author.full_clean()  # Run model validations
            author.save()
            
            return UpdateAuthor(success=True, message="Author updated successfully", author=author)
        except Author.DoesNotExist:
            return UpdateAuthor(success=False, message=f"Author with ID {id} not found", author=None)
        except ValidationError as e:
            return UpdateAuthor(success=False, message=str(e), author=None)
        except Exception as e:
            return UpdateAuthor(success=False, message=f"Error: {str(e)}", author=None)


class DeleteAuthor(graphene.Mutation):
    """Delete an author."""
    
    class Arguments:
        id = Int(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id):
        try:
            author = Author.objects.get(pk=id)
            author.delete()
            return DeleteAuthor(success=True, message="Author deleted successfully")
        except Author.DoesNotExist:
            return DeleteAuthor(success=False, message=f"Author with ID {id} not found")
        except Exception as e:
            return DeleteAuthor(success=False, message=f"Error: {str(e)}")


class CreatePublisher(graphene.Mutation):
    """Create a new publisher."""
    
    class Arguments:
        input = PublisherInput(required=True)
    
    publisher = graphene.Field(PublisherType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        try:
            if Publisher.objects.filter(name=input.name).exists():
                return CreatePublisher(success=False, message="Publisher name already exists", publisher=None)
            
            publisher = Publisher.objects.create(
                name=input.name,
                country=input.country,
                established_year=input.established_year
            )
            
            return CreatePublisher(success=True, message="Publisher created successfully", publisher=publisher)
        except Exception as e:
            return CreatePublisher(success=False, message=f"Error: {str(e)}", publisher=None)


class CreateBook(graphene.Mutation):
    """Create a new book."""
    
    class Arguments:
        input = BookInput(required=True)
    
    book = graphene.Field(BookType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        try:
            # Check if author exists
            try:
                author = Author.objects.get(pk=input.author_id)
            except Author.DoesNotExist:
                return CreateBook(success=False, message=f"Author with ID {input.author_id} not found", book=None)
            
            # Check if publisher exists (optional)
            publisher = None
            if input.publisher_id:
                try:
                    publisher = Publisher.objects.get(pk=input.publisher_id)
                except Publisher.DoesNotExist:
                    return CreateBook(success=False, message=f"Publisher with ID {input.publisher_id} not found", book=None)
            
            # Check ISBN uniqueness
            if input.isbn and Book.objects.filter(isbn=input.isbn).exists():
                return CreateBook(success=False, message="ISBN already exists", book=None)
            
            book = Book.objects.create(
                title=input.title,
                description=input.description,
                author=author,
                publisher=publisher,
                published_date=input.published_date,
                pages=input.pages,
                isbn=input.isbn
            )
            book.full_clean()  # Run model validations
            book.save()
            
            return CreateBook(success=True, message="Book created successfully", book=book)
        except ValidationError as e:
            return CreateBook(success=False, message=str(e), book=None)
        except Exception as e:
            return CreateBook(success=False, message=f"Error: {str(e)}", book=None)


class UpdateBook(graphene.Mutation):
    """Update an existing book."""
    
    class Arguments:
        id = Int(required=True)
        input = BookInput(required=True)
    
    book = graphene.Field(BookType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id, input):
        try:
            book = Book.objects.get(pk=id)
            
            # Check author
            try:
                author = Author.objects.get(pk=input.author_id)
            except Author.DoesNotExist:
                return UpdateBook(success=False, message=f"Author with ID {input.author_id} not found", book=None)
            
            # Check publisher (optional)
            publisher = None
            if input.publisher_id:
                try:
                    publisher = Publisher.objects.get(pk=input.publisher_id)
                except Publisher.DoesNotExist:
                    return UpdateBook(success=False, message=f"Publisher with ID {input.publisher_id} not found", book=None)
            
            # Check ISBN uniqueness (if different from current)
            if input.isbn and input.isbn != book.isbn and Book.objects.filter(isbn=input.isbn).exists():
                return UpdateBook(success=False, message="ISBN already exists", book=None)
            
            book.title = input.title
            book.description = input.description
            book.author = author
            book.publisher = publisher
            book.published_date = input.published_date
            if input.pages:
                book.pages = input.pages
            if input.isbn:
                book.isbn = input.isbn
            
            book.full_clean()  # Run model validations
            book.save()
            
            return UpdateBook(success=True, message="Book updated successfully", book=book)
        except Book.DoesNotExist:
            return UpdateBook(success=False, message=f"Book with ID {id} not found", book=None)
        except ValidationError as e:
            return UpdateBook(success=False, message=str(e), book=None)
        except Exception as e:
            return UpdateBook(success=False, message=f"Error: {str(e)}", book=None)


class DeleteBook(graphene.Mutation):
    """Delete a book."""
    
    class Arguments:
        id = Int(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True, message="Book deleted successfully")
        except Book.DoesNotExist:
            return DeleteBook(success=False, message=f"Book with ID {id} not found")
        except Exception as e:
            return DeleteBook(success=False, message=f"Error: {str(e)}")


class CreateReview(graphene.Mutation):
    """Create a review for a book."""
    
    class Arguments:
        input = ReviewInput(required=True)
    
    review = graphene.Field(ReviewType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        try:
            # Check if book exists
            try:
                book = Book.objects.get(pk=input.book_id)
            except Book.DoesNotExist:
                return CreateReview(success=False, message=f"Book with ID {input.book_id} not found", review=None)
            
            # Check if book already has a review
            if Review.objects.filter(book=book).exists():
                return CreateReview(success=False, message="This book already has a review", review=None)
            
            # Validate rating
            if input.rating < 1 or input.rating > 5:
                return CreateReview(success=False, message="Rating must be between 1 and 5", review=None)
            
            review = Review.objects.create(
                book=book,
                rating=input.rating,
                review_text=input.review_text,
                reviewer_name=input.reviewer_name
            )
            review.full_clean()  # Run model validations
            review.save()
            
            return CreateReview(success=True, message="Review created successfully", review=review)
        except ValidationError as e:
            return CreateReview(success=False, message=str(e), review=None)
        except Exception as e:
            return CreateReview(success=False, message=f"Error: {str(e)}", review=None)


class UpdateReview(graphene.Mutation):
    """Update an existing review."""
    
    class Arguments:
        id = Int(required=True)
        input = ReviewInput(required=True)
    
    review = graphene.Field(ReviewType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id, input):
        try:
            review = Review.objects.get(pk=id)
            
            # Validate rating
            if input.rating < 1 or input.rating > 5:
                return UpdateReview(success=False, message="Rating must be between 1 and 5", review=None)
            
            review.rating = input.rating
            review.review_text = input.review_text
            review.reviewer_name = input.reviewer_name
            
            review.full_clean()  # Run model validations
            review.save()
            
            return UpdateReview(success=True, message="Review updated successfully", review=review)
        except Review.DoesNotExist:
            return UpdateReview(success=False, message=f"Review with ID {id} not found", review=None)
        except ValidationError as e:
            return UpdateReview(success=False, message=str(e), review=None)
        except Exception as e:
            return UpdateReview(success=False, message=f"Error: {str(e)}", review=None)


class DeleteReview(graphene.Mutation):
    """Delete a review."""
    
    class Arguments:
        id = Int(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, id):
        try:
            review = Review.objects.get(pk=id)
            review.delete()
            return DeleteReview(success=True, message="Review deleted successfully")
        except Review.DoesNotExist:
            return DeleteReview(success=False, message=f"Review with ID {id} not found")
        except Exception as e:
            return DeleteReview(success=False, message=f"Error: {str(e)}")


# =====================================================================
# Root Query and Mutation Types
# =====================================================================

class Query(graphene.ObjectType):
    """Root Query type - read operations."""
    
    # Authors
    all_authors = graphene.List(AuthorType, description="Get all authors")
    author = graphene.Field(AuthorType, id=graphene.Int(required=True), description="Get author by ID")
    
    # Books
    all_books = graphene.List(BookType, description="Get all books")
    book = graphene.Field(BookType, id=graphene.Int(required=True), description="Get book by ID")
    
    # Publishers
    all_publishers = graphene.List(PublisherType, description="Get all publishers")
    publisher = graphene.Field(PublisherType, id=graphene.Int(required=True), description="Get publisher by ID")
    
    # Reviews
    all_reviews = graphene.List(ReviewType, description="Get all reviews")
    review = graphene.Field(ReviewType, id=graphene.Int(required=True), description="Get review by ID")
    
    # Resolvers
    def resolve_all_authors(self, info):
        return Author.objects.all()
    
    def resolve_author(self, info, id):
        try:
            return Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return None
    
    def resolve_all_books(self, info):
        return Book.objects.select_related('author', 'publisher').all()
    
    def resolve_book(self, info, id):
        try:
            return Book.objects.select_related('author', 'publisher').get(pk=id)
        except Book.DoesNotExist:
            return None
    
    def resolve_all_publishers(self, info):
        return Publisher.objects.all()
    
    def resolve_publisher(self, info, id):
        try:
            return Publisher.objects.get(pk=id)
        except Publisher.DoesNotExist:
            return None
    
    def resolve_all_reviews(self, info):
        return Review.objects.select_related('book').all()
    
    def resolve_review(self, info, id):
        try:
            return Review.objects.select_related('book').get(pk=id)
        except Review.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    """Root Mutation type - write operations."""
    
    # Author mutations
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
    
    # Publisher mutations
    create_publisher = CreatePublisher.Field()
    
    # Book mutations
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    
    # Review mutations
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    delete_review = DeleteReview.Field()


# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
