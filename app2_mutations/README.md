# App 2: Mutations, Validation & Relationships

This is the second app in the GraphQL with Django and Graphene learning path. It covers mutations for creating, updating, and deleting data, plus relationships between models.

## Topics Covered

✅ Mutations (Create, Update, Delete operations)  
✅ Input types for mutations  
✅ Data validation and error handling  
✅ ForeignKey relationships  
✅ OneToOne relationships  
✅ ManyToMany relationships  
✅ Nested queries with relationships  
✅ Exception handling in mutations  

## Learning Outcomes

- Understand GraphQL mutations
- Create, update, and delete data via GraphQL
- Validate input data on the server
- Handle errors gracefully
- Query related data with nested queries
- Build complex relationships between models

---

## Project Structure

```
app2_mutations/
├── config/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   └── schema.py            # GraphQL schema with mutations
├── mutations_app/
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── models.py            # Django models
│   ├── apps.py
│   ├── admin.py
│   └── tests.py
├── manage.py
├── requirements.txt         # Project dependencies
├── add_sample_data.py      # Sample data script
├── README.md               # This file
├── QUICKSTART.md           # Quick setup guide
└── postman/                # Postman collection
```

---

## Installation & Setup

### 1. Create Virtual Environment

```bash
cd app2_mutations
python -m venv venv
venv\Scripts\activate  # On Windows
# OR: source venv/bin/activate (On Mac/Linux)
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations

```bash
python manage.py migrate
```

### 4. Create Django Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 5. Add Sample Data

```bash
python manage.py shell < add_sample_data.py
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

---

## Accessing GraphQL Interface

### GraphiQL Interface
Open your browser and go to:
```
http://127.0.0.1:8000/graphql/
```

This provides an interactive GraphQL editor where you can write and test queries and mutations.

---

## Models & Database Schema

### Publisher Model
```python
class Publisher(models.Model):
    name = CharField(max_length=200, unique=True)
    country = CharField(max_length=100)
    established_year = IntegerField()
```

### Author Model
```python
class Author(models.Model):
    name = CharField(max_length=200)
    email = EmailField(unique=True)
    bio = TextField(blank=True)
    birth_year = IntegerField(null=True, blank=True)
    publishers = ManyToManyField(Publisher)  # Many-to-Many
```

### Book Model
```python
class Book(models.Model):
    title = CharField(max_length=300)
    description = TextField()
    author = ForeignKey(Author)      # One-to-Many
    publisher = ForeignKey(Publisher)  # One-to-Many
    published_date = DateField()
    pages = IntegerField(blank=True)
    isbn = CharField(max_length=20, unique=True, blank=True)
```

### Review Model
```python
class Review(models.Model):
    book = OneToOneField(Book)        # One-to-One
    rating = IntegerField(choices=1-5)
    review_text = TextField()
    reviewer_name = CharField(max_length=200)
```

---

## Relationships Overview

```
Publisher
    ├─ 1 : Many ─────────→ Author (via ManyToMany)
    └─ 1 : Many ─────────→ Book

Author
    ├─ 1 : Many ─────────→ Book
    └─ Many : 1 ←──────── Publisher (via ManyToMany)

Book
    ├─ Many : 1 ←──────── Author
    ├─ Many : 1 ←──────── Publisher
    └─ 1 : 1 ────────────→ Review
```

---

## GraphQL Queries Examples

### 1. Get All Authors with Publishers

```graphql
{
  allAuthors {
    id
    name
    email
    bio
    birthYear
    publishers {
      id
      name
      country
    }
  }
}
```

### 2. Get All Books with Author and Publisher

```graphql
{
  allBooks {
    id
    title
    description
    author {
      id
      name
      email
    }
    publisher {
      id
      name
      country
    }
    publishedDate
    pages
    isbn
  }
}
```

### 3. Get Book with Review

```graphql
{
  book(id: 1) {
    id
    title
    author {
      name
    }
    review {
      rating
      reviewText
      reviewerName
    }
  }
}
```

### 4. Get Author with All Books

```graphql
{
  author(id: 1) {
    id
    name
    email
    bio
    books {
      id
      title
      publishedDate
    }
  }
}
```

---

## Mutations Examples

### 1. Create Author

```graphql
mutation {
  createAuthor(input: {
    name: "Stephen King"
    email: "stephen.king@example.com"
    bio: "American author known for horror novels"
    birthYear: 1947
  }) {
    author {
      id
      name
      email
    }
    success
    message
  }
}
```

### 2. Update Author

```graphql
mutation {
  updateAuthor(id: 1, input: {
    name: "J.K. Rowling"
    email: "jk.rowling@example.com"
    bio: "British author and creator of Harry Potter"
    birthYear: 1965
  }) {
    author {
      id
      name
      email
    }
    success
    message
  }
}
```

### 3. Delete Author

```graphql
mutation {
  deleteAuthor(id: 1) {
    success
    message
  }
}
```

### 4. Create Book

```graphql
mutation {
  createBook(input: {
    title: "The Stand"
    description: "A post-apocalyptic novel"
    authorId: 4
    publisherId: 2
    publishedDate: "1978-10-03"
    pages: 823
    isbn: "978-0385193696"
  }) {
    book {
      id
      title
      author {
        name
      }
      publisher {
        name
      }
    }
    success
    message
  }
}
```

### 5. Create Review

```graphql
mutation {
  createReview(input: {
    bookId: 1
    rating: 5
    reviewText: "An amazing book! Highly recommended."
    reviewerName: "John Doe"
  }) {
    review {
      id
      book {
        title
      }
      rating
      reviewText
      reviewerName
    }
    success
    message
  }
}
```

### 6. Update Review

```graphql
mutation {
  updateReview(id: 1, input: {
    bookId: 1
    rating: 4
    reviewText: "Great book with some slow parts"
    reviewerName: "John Doe"
  }) {
    review {
      id
      rating
      reviewText
    }
    success
    message
  }
}
```

### 7. Delete Review

```graphql
mutation {
  deleteReview(id: 1) {
    success
    message
  }
}
```

---

## Error Handling

All mutations return both success status and messages:

```graphql
mutation {
  createAuthor(input: {
    name: "Test Author"
    email: "duplicate@example.com"  # Already exists
    bio: ""
    birthYear: null
  }) {
    success      # false
    message      # "Email already exists"
    author       # null
  }
}
```

### Validation Errors

- **Email uniqueness**: Authors cannot have duplicate emails
- **Birth year**: Cannot be in the future
- **Book pages**: Must be greater than 0
- **Review rating**: Must be between 1 and 5
- **ISBN uniqueness**: Books cannot have duplicate ISBNs

---

## Key Concepts

### Mutations
GraphQL operations that modify data (CREATE, UPDATE, DELETE).

### Input Types
Structured input for mutations - ensures all required fields are provided and validates data.

### Relationships
- **ForeignKey**: One-to-Many relationship (Book → Author)
- **OneToOne**: One-to-One relationship (Book → Review)
- **ManyToMany**: Many-to-Many relationship (Author ↔ Publisher)

### Nested Queries
Query related data in a single request:
```graphql
{
  book(id: 1) {
    title
    author {      # Nested
      name
    }
  }
}
```

### Error Handling
Mutations return structured responses with success flag and error messages for client-side handling.

---

## Testing

### Using GraphiQL
1. Open http://127.0.0.1:8000/graphql/
2. Copy any mutation from examples above
3. Click Play/Send button
4. View results on the right panel

### Using Postman
Import the collection from the `postman/` folder for pre-configured requests.

---

## Commands Reference

```bash
# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Open Django shell
python manage.py shell

# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Access Django admin
# http://127.0.0.1:8000/admin/
```

---

## Common Issues & Solutions

### "Author with ID X not found"
**Solution:** Check the author ID exists. Run in shell:
```python
from mutations_app.models import Author
Author.objects.all().values('id', 'name')
```

### "Email already exists"
**Solution:** Use a unique email for new authors

### "Rating must be between 1 and 5"
**Solution:** Provide a rating value from 1 to 5

### "Book already has a review"
**Solution:** Each book can only have one review. Try updating existing review instead.

---

## Next Steps

After mastering this app, proceed to **App 3: Filtering, Sorting, Pagination & Advanced Queries** to learn:
- Advanced filtering options
- Sorting and ordering
- Pagination strategies
- Complex query patterns

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Permission Denied on Migrations
```bash
python manage.py makemigrations mutations_app
python manage.py migrate
```

### GraphQL Endpoint Not Working
Ensure `config.urls` is properly configured and make sure Django settings include the schema path.

---

## Additional Resources

- [Graphene Documentation](https://docs.graphene-python.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [GraphQL Official Documentation](https://graphql.org/learn/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

