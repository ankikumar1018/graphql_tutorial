# Quick Start Guide - App 2: Mutations

## ⚡ Get Started in 5 Minutes

First ensure you have Python 3.8+ installed.

### Step 1: Create Virtual Environment
```bash
cd app2_mutations
python -m venv venv
venv\Scripts\activate  # On Windows
# OR: source venv/bin/activate (On Mac/Linux)
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Add Sample Data
```bash
python manage.py shell < add_sample_data.py
```

### Step 5: Start Development Server
```bash
python manage.py runserver
```

### Step 6: Test GraphQL
Open your browser and go to:
```
http://127.0.0.1:8000/graphql/
```

---

## 🚀 Your First Mutation

### Create an Author
Copy this into the GraphQL editor and press play:

```graphql
mutation {
  createAuthor(input: {
    name: "Stephen King"
    email: "stephen.king@example.com"
    bio: "American horror author"
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

---

## 📚 Key Concepts

### What is a Mutation?
A **mutation** is an operation that **modifies data** (Create, Update, Delete).

### Input Types
Mutations accept **input objects** with required and optional fields.

### Response Structure
Mutations return:
- `success`: Boolean indicating if operation succeeded
- `message`: Human-readable message
- `author` (or other data): The created/updated object

---

## 🔥 Quick Examples

### Try These Mutations:

**Update an Author:**
```graphql
mutation {
  updateAuthor(id: 1, input: {
    name: "J.K. Rowling"
    email: "jk@example.com"
    bio: "Creator of Harry Potter"
    birthYear: 1965
  }) {
    success
    message
  }
}
```

**Create a Book:**
```graphql
mutation {
  createBook(input: {
    title: "It"
    description: "A horror novel set in a small town"
    authorId: 1
    publishedDate: "1986-05-15"
    pages: 1138
    isbn: "978-0451169518"
  }) {
    book {
      id
      title
      author {
        name
      }
    }
    success
    message
  }
}
```

**Create a Review:**
```graphql
mutation {
  createReview(input: {
    bookId: 1
    rating: 5
    reviewText: "Amazing book!"
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

**Delete a Book:**
```graphql
mutation {
  deleteBook(id: 1) {
    success
    message
  }
}
```

---

## 🔄 Query Examples

**Get all books with author info:**
```graphql
{
  allBooks {
    id
    title
    author {
      name
      email
    }
    publisher {
      name
    }
  }
}
```

**Get a book with its review:**
```graphql
{
  book(id: 1) {
    title
    author {
      name
    }
    review {
      rating
      reviewText
    }
  }
}
```

**Get author with all their books:**
```graphql
{
  author(id: 1) {
    name
    books {
      title
      publishedDate
    }
  }
}
```

---

## 📋 Available Mutations

### Author Mutations
- `createAuthor` - Create new author
- `updateAuthor` - Update existing author
- `deleteAuthor` - Delete author

### Publisher Mutations
- `createPublisher` - Create new publisher

### Book Mutations
- `createBook` - Create new book
- `updateBook` - Update existing book
- `deleteBook` - Delete book

### Review Mutations
- `createReview` - Create review for a book
- `updateReview` - Update existing review
- `deleteReview` - Delete review

---

## 🆘 Troubleshooting

### "Email already exists"
Solution: Use a different email address

### "Author with ID X not found"
Solution: Check the ID exists by querying all authors first

### "Book already has a review"
Solution: Update the existing review instead of creating a new one

### Port 8000 already in use?
```bash
python manage.py runserver 8001
```

---

## 💡 Pro Tips

1. **Get auto-complete in GraphiQL:**
   - Press `Ctrl+Space` to see available fields and mutations

2. **View schema documentation:**
   - Click the "Docs" tab on the right panel in GraphiQL

3. **Test errors:**
   - Try creating author with email that already exists
   - Try rating book review with rating 10 (invalid)

4. **Combine queries and mutations:**
   - Create an author and immediately query it

---

## 📚 Next Steps

1. Try all mutation examples above
2. Create your own data
3. Test error handling (invalid inputs)
4. Query nested relationships
5. Move to App 3: Filtering & Pagination

---

## 📁 Important Files

- [README.md](README.md) - Complete documentation
- [schema.py](config/schema.py) - All mutations and queries
- [models.py](mutations_app/models.py) - Data models

---

Ready to create data? Start with the "Create an Author" example above! 🚀
