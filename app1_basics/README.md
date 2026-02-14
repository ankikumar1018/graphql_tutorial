# App 1: GraphQL Basics & Django Models

This is the first app in the GraphQL with Django and Graphene learning path. It covers the fundamentals of GraphQL and how to query Django models.

## Topics Covered

✅ GraphQL fundamentals  
✅ Setup & installation  
✅ Basic queries  
✅ Define ObjectType  
✅ Create Root Query  
✅ Django models integration  
✅ Query single objects  
✅ Query lists of objects  
✅ Model fields mapping  
✅ Test in GraphiQL  

## Learning Outcomes

- Understand GraphQL basics
- Set up Graphene with Django
- Create your first GraphQL API
- Query Django models

---

## Project Structure

```
app1_basics/
├── config/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration (GraphQL endpoint)
│   └── schema.py            # GraphQL schema definition
├── basics_app/
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── models.py            # Django models (Author, Book)
│   ├── apps.py
│   ├── admin.py
├── manage.py
├── requirements.txt         # Project dependencies
└── README.md
```

## Installation & Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
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

### 5. Run the Development Server

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

This provides an interactive GraphQL editor where you can write and test queries.

---

## GraphQL Queries Examples

### 1. Get All Authors

```graphql
{
  allAuthors {
    id
    name
    email
    createdAt
  }
}
```

### 2. Get Single Author by ID

```graphql
{
  author(id: 1) {
    id
    name
    email
  }
}
```

### 3. Get All Books

```graphql
{
  allBooks {
    id
    title
    description
    author {
      id
      name
    }
    publishedDate
  }
}
```

### 4. Get Single Book by ID

```graphql
{
  book(id: 1) {
    id
    title
    description
    author {
      id
      name
      email
    }
    publishedDate
  }
}
```

### 5. Get Books with Author Details

```graphql
{
  allBooks {
    id
    title
    author {
      name
      email
    }
    publishedDate
  }
}
```

---

## Django Models

### Author Model

```python
class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Book Model

```python
class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## GraphQL Schema

### ObjectTypes

```python
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'created_at']

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'published_date', 'created_at']
```

### Root Query

```python
class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.Int(required=True))
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int(required=True))
```

---

## Key Concepts

### 1. ObjectType
Converts Django models into GraphQL types. Each field in the model becomes a field in the GraphQL type.

### 2. Query
The entry point for all read operations in GraphQL. Defines what data can be queried.

### 3. Resolver
A function that resolves the value for a field. It determines how to fetch data from the database.

### 4. Schema
The complete definition of the GraphQL API - what queries are available and what they return.

### 5. GraphiQL
An interactive web-based IDE for exploring and testing GraphQL queries.

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

# Access SQL queries in shell
python manage.py sqlmigrate basics_app 0001
```

---

## Next Steps

After mastering this app, proceed to **App 2: Mutations, Validation & Relationships** to learn how to:
- Create, update, and delete data
- Validate input data
- Handle relationships between models
- Implement mutations

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Permission Denied on Migrations
```bash
python manage.py makemigrations basics_app
python manage.py migrate
```

### GraphQL Endpoint Not Working
Ensure `config.urls` is properly configured and the Django settings include the schema path.

---

## Additional Resources

- [Graphene Documentation](https://docs.graphene-python.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [GraphQL Official Documentation](https://graphql.org/learn/)

