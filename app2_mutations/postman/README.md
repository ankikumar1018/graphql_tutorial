# Postman Collection - App 2: Mutations, Validation & Relationships

This folder contains a Postman collection for testing all GraphQL mutations and queries in App 2.

## 📥 How to Import

### Method 1: Drag & Drop
1. Open Postman
2. Drag and drop `GraphQL-App2-Collection.json` into Postman
3. The collection will be imported automatically

### Method 2: Import Button
1. Open Postman
2. Click the **Import** button (top left)
3. Select **Upload Files**
4. Choose `GraphQL-App2-Collection.json`
5. Click **Import**

---

## ✅ Setup Required

Before running any requests:

1. **Django server is running**
   ```bash
   cd app2_mutations
   python manage.py runserver
   ```

2. **Database is migrated and populated**
   ```bash
   python manage.py migrate
   python manage.py shell < add_sample_data.py
   ```

3. **Server running at** `http://127.0.0.1:8000/`

---

## 📦 Collection Contents

### 1. **Query Examples** (6 requests)
- ✅ Get All Authors with Publishers
- ✅ Get All Books with Author and Publisher
- ✅ Get Book with Review
- ✅ Get Author with All Books
- ✅ Get All Publishers
- ✅ Get All Reviews

### 2. **Create Mutations** (4 requests)
- ✅ Create Author
- ✅ Create Publisher
- ✅ Create Book
- ✅ Create Review

### 3. **Update Mutations** (3 requests)
- ✅ Update Author
- ✅ Update Book
- ✅ Update Review

### 4. **Delete Mutations** (3 requests)
- ✅ Delete Author
- ✅ Delete Book
- ✅ Delete Review

### 5. **Error Testing** (4 requests)
- ✅ Create Author - Duplicate Email
- ✅ Create Book - Invalid Author ID
- ✅ Create Review - Invalid Rating
- ✅ Delete Non-existent Author

**Total: 20 Pre-configured Requests**

---

## 🚀 Quick Start

1. **Import the collection** (follow import steps above)
2. **Ensure server is running** on `http://127.0.0.1:8000/`
3. **Click any request** in the collection
4. **Click Send button**
5. **See response** on the right panel

---

## 🔧 Hardcoded Settings

✅ **URL:** All requests point to `http://127.0.0.1:8000/graphql/`  
✅ **Method:** All requests use POST  
✅ **Content-Type:** application/json  
✅ **No environment variables needed**  

---

## 💡 Tips for Using Postman

### Modifying Mutations
1. Click on any mutation request
2. Edit the mutation parameters in the **Body** section
3. Click **Send** to test
4. View response immediately

### Testing with Different IDs
- Change `id: 1` to any other number
- Change `authorId: 1` to test with different authors
- Change `bookId: 1` to test with different books

### Understanding Error Messages
- "Email already exists" - Email is not unique
- "Author with ID X not found" - Invalid ID
- "Rating must be between 1 and 5" - Invalid rating value

---

## 📊 Sample Data Structure

### Authors (Created)
- ID: 1 - J.K. Rowling
- ID: 2 - George R.R. Martin
- ID: 3 - J.R.R. Tolkien

### Publishers (Created)
- ID: 1 - Bloomsbury Publishing
- ID: 2 - Bantam Books
- ID: 3 - HarperCollins

### Books (Created)
- ID: 1 - Harry Potter and the Philosopher Stone (Author: 1)
- ID: 2 - A Game of Thrones (Author: 2)
- ID: 3 - The Hobbit (Author: 3)

### Reviews (Created)
- ID: 1 - Book 1 - Rating: 5
- ID: 2 - Book 3 - Rating: 5

---

## 🔄 Example Workflow

### Create and Verify Flow:

1. **Create Author (Create Mutations → Create Author)**
   - Modify email and name
   - Send request
   - Note the returned ID

2. **Create Book (Create Mutations → Create Book)**
   - Use the author ID from step 1
   - Change `authorId: 1` to your author ID
   - Send request

3. **Get All Books (Query Examples → Get All Books...)**
   - Send request
   - Verify your new book appears

4. **Update Book (Update Mutations → Update Book)**
   - Change the ID and fields
   - Send request

5. **Delete Book (Delete Mutations → Delete Book)**
   - Send request
   - Verify deletion

---

## 🆘 Troubleshooting

### "Cannot connect to http://127.0.0.1:8000/graphql/"
**Solution:** Ensure Django server is running
```bash
python manage.py runserver
```

### "Author with ID X not found"
**Solution:** Check the ID exists
- Run Query Examples → Get All Authors
- Use an ID from the results

### "Email already exists"
**Solution:** Use a unique email address

### "Book already has a review"
**Solution:** Each book can only have one review
- Delete the existing review first, or
- Update the existing review instead

---

## 📚 Key Relationships Tested

| Relationship | Example |
|--------------|---------|
| **ForeignKey** | Book → Author |
| **OneToOne** | Book → Review |
| **ManyToMany** | Author ↔ Publisher |

---

## 🎯 Learning Objectives

After using this collection, you'll understand:
- ✅ How to perform CRUD operations via GraphQL
- ✅ How to validate input data
- ✅ How to handle errors gracefully
- ✅ How to query related data
- ✅ How nested queries work

---

## 📄 Collection Metadata

- **Name:** GraphQL App 2 - Mutations, Validation & Relationships
- **Requests:** 20 pre-configured mutations and queries
- **Endpoint:** http://127.0.0.1:8000/graphql/
- **Environment:** None required (everything hardcoded)

---

## 📖 Related Documentation

- [App 2 README](../README.md) - Complete API documentation
- [Quick Start Guide](../QUICKSTART.md) - Setup instructions
- [Schema Details](../config/schema.py) - Schema definition

---

**Ready to test mutations?** Import the collection and start with "Create Author"! 🚀
