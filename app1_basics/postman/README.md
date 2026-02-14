# Postman Collection - App 1: GraphQL Basics & Django Models

This folder contains a Postman collection for testing all GraphQL queries in App 1.

## 📥 How to Import

### Method 1: Drag & Drop
1. Open Postman (https://www.postman.com/downloads/)
2. Click **Workspace** → **My Workspace**
3. Drag and drop `GraphQL-App1-Collection.json` into Postman
4. The collection will be imported automatically

### Method 2: Import Button
1. Open Postman
2. Click the **Import** button (top left)
3. Select **Upload Files**
4. Choose `GraphQL-App1-Collection.json`
5. Click **Import**

---

## ✅ Setup Required

Before running any requests, ensure:

1. **Django server is running**
   ```bash
   cd app1_basics
   python manage.py runserver
   ```

2. **Database is migrated and populated**
   ```bash
   python manage.py migrate
   python manage.py shell < add_sample_data.py
   ```

3. **Server should be running at** `http://127.0.0.1:8000/`

---

## 📦 Collection Contents

### 1. **Author Queries** (4 requests)
- ✅ Get All Authors
- ✅ Get Author by ID (ID: 1)
- ✅ Get Author by ID (ID: 2)
- ✅ Get Authors with Book Count

### 2. **Book Queries** (5 requests)
- ✅ Get All Books
- ✅ Get All Books (Minimal Fields)
- ✅ Get Book by ID (ID: 1)
- ✅ Get Book by ID (ID: 2)
- ✅ Get All Books with Full Author Info

### 3. **Combined Queries** (2 requests)
- ✅ Get Authors and Books Together
- ✅ Get Specific Author and Specific Book

### 4. **Testing Relationships** (2 requests)
- ✅ Get Author 1 and All Books by That Author
- ✅ Get All Books (Extended Info)

### 5. **Error Testing** (2 requests)
- ✅ Get Author with Invalid ID (ID: 999)
- ✅ Get Book with Invalid ID (ID: 999)

**Total: 15 Pre-configured GraphQL Queries**

---

## 🚀 Quick Start

1. **Import the collection** (follow steps above)
2. **Ensure server is running** on `http://127.0.0.1:8000/`
3. **Click any request** in the collection
4. **Click the Send button**
5. **See the GraphQL response** on the right panel

---

## 🔧 Hardcoded Settings

✅ **URL:** All requests point to `http://127.0.0.1:8000/graphql/`  
✅ **Method:** All requests use POST  
✅ **Content-Type:** application/json  
✅ **No environment variables needed**  

Everything is ready to use out of the box!

---

## 📝 Example Request

**Name:** Get All Authors  
**URL:** http://127.0.0.1:8000/graphql/  
**Method:** POST  
**Body (GraphQL):**
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

---

## 💡 Tips for Using Postman

### Viewing Response Data
- Click the **Body** tab in the response panel
- Switch between **Pretty**, **Raw**, and **Preview** views
- Use **JSON** format for better readability

### Modifying Queries
1. Click on any request in the collection
2. Edit the GraphQL query in the **Body** section
3. Click **Send** to test your changes
4. The response appears in the right panel

### Testing Different IDs
1. Click on a request like "Get Author by ID (ID: 1)"
2. In the Body section, change `id: 1` to any other ID
3. Click **Send**

### Organizing Tests
- Create folders within the collection for different query types
- Use naming conventions to keep requests organized
- Add descriptive names to custom queries

---

## 🔄 Sample Data Structure

### Authors (Sample Data)
- ID: 1 - J.K. Rowling (jk.rowling@example.com)
- ID: 2 - George R.R. Martin (george.martin@example.com)
- ID: 3 - J.R.R. Tolkien (jrr.tolkien@example.com)

### Books (Sample Data)
- ID: 1 - Harry Potter and the Philosopher Stone (Author ID: 1)
- ID: 2 - Harry Potter and the Chamber of Secrets (Author ID: 1)
- ID: 3 - A Game of Thrones (Author ID: 2)
- ID: 4 - A Clash of Kings (Author ID: 2)
- ID: 5 - The Hobbit (Author ID: 3)

---

## 🆘 Troubleshooting

### "Cannot connect to http://127.0.0.1:8000/graphql/"
**Solution:** Ensure Django server is running
```bash
python manage.py runserver
```

### "Null or empty response"
**Solution:** Ensure sample data is loaded
```bash
python manage.py shell < add_sample_data.py
```

### "CORS error"
**Solution:** Not applicable for this setup - requests are from the same origin

### Query returns null
**Solution:** Check the ID exists in the database
- Run: `python manage.py shell`
- Type: `from basics_app.models import Author; Author.objects.all()`

---

## 📚 Related Documentation

- [App 1 README](../README.md) - Full API documentation
- [Quick Start Guide](../QUICKSTART.md) - Setup instructions
- [GraphQL Documentation](../config/schema.py) - Schema details

---

## 🎯 Next Steps

After testing all queries:
1. Modify queries to fetch different fields
2. Test combining multiple queries
3. Try the error cases with invalid IDs
4. Review the schema in GraphiQL: http://127.0.0.1:8000/graphql/

---

## 📄 Collection Details

- **Name:** GraphQL App 1 - Basics & Django Models
- **Requests:** 15 pre-configured queries
- **Endpoint:** http://127.0.0.1:8000/graphql/
- **Environment:** None required (everything hardcoded)
- **Last Updated:** 2026-02-11

---

**Ready to test?** Import the collection and start sending requests! 🚀
