# Quick Start Guide - App 1

## ⚡ Get Started in 5 Minutes

First ensure you have Python 3.8+ installed.

### Step 1: Create Virtual Environment
```bash
cd app1_basics
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

## 🚀 Your First GraphQL Query

Copy this into the GraphQL editor and press play:

```graphql
{
  allAuthors {
    id
    name
    email
  }
}
```

### Try These Queries:

**Get all books with authors:**
```graphql
{
  allBooks {
    id
    title
    description
    author {
      name
    }
  }
}
```

**Get a specific author:**
```graphql
{
  author(id: 1) {
    name
    email
  }
}
```

**Get a specific book:**
```graphql
{
  book(id: 1) {
    title
    author {
      name
      email
    }
  }
}
```

---

## 📚 Key Files to Review

1. **models.py** - Understand the Author and Book models
2. **schema.py** - See how models are converted to GraphQL types
3. **settings.py** - Django configuration and Graphene setup
4. **urls.py** - GraphQL endpoint configuration

---

## 🔍 Interactive Testing

In the GraphQL editor, you can:
- Write queries
- Get auto-complete suggestions (Ctrl+Space)
- View schema documentation (right panel)
- See query results in real-time

---

## 💡 Learning Tips

1. Open the "Docs" tab on the right in GraphiQL to explore the schema
2. Look at the example queries in README.md
3. Try modifying queries to fetch different fields
4. Check the Django shell to see SQL queries: `python manage.py shell`

---

## ❓ Troubleshooting

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Database issues?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py shell < add_sample_data.py
```

---

Ready to learn? Start with the GraphQL queries above! 🎉
