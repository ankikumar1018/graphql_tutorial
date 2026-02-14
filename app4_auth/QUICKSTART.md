# App 4 Quick Start Guide

Get up and running with JWT authentication and permissions in 5 minutes.

## Installation

### 1. Install Dependencies
```bash
cd app4_auth
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Data (includes admin user)
```bash
python manage.py shell < add_sample_data.py
```

Output:
```
✅ Sample data created successfully!
Created 3 users (admin, moderator, user)
Created 5 posts with various statuses
Created 8 comments
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Server: **http://localhost:8000/graphql/**

## First Steps

### 1. Test Registration

Open Postman or GraphQL IDE, send this mutation:

```graphql
mutation RegisterUser($input: UserRegisterInput!) {
  register(input: $input) {
    success
    message
    user {
      id
      username
    }
    token
  }
}
```

Variables:
```json
{
  "input": {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "firstName": "Test",
    "lastName": "User"
  }
}
```

Response:
```json
{
  "data": {
    "register": {
      "success": true,
      "message": "User registered successfully",
      "user": {
        "id": "4",
        "username": "testuser"
      },
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
}
```

**Save the token** - you'll use it for authenticated requests!

### 2. Test Login

```graphql
mutation LoginUser($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    success
    message
    user {
      id
      username
    }
    token
  }
}
```

Variables:
```json
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

## Essential Queries

### 1. Public Queries (No Token Needed)

**Get all published posts:**
```graphql
{
  allPosts {
    id
    title
    authorName
    commentCount
    createdAt
  }
}
```

**Get specific post with comments:**
```graphql
{
  post(id: 1) {
    id
    title
    content
    authorName
    comments {
      text
      authorName
      createdAt
    }
  }
}
```

**Get user by username:**
```graphql
{
  userByUsername(username: "admin") {
    id
    username
    profile {
      role
      bio
    }
  }
}
```

### 2. Authenticated Queries (Token Required)

**Get current user:**
```graphql
{
  me {
    id
    username
    email
    profile {
      role
      bio
    }
  }
}
```

**Add header:** `Authorization: Bearer <your_token>`

**Get my posts:**
```graphql
{
  myPosts {
    id
    title
    status
    canEdit
    canDelete
  }
}
```

**Get my activity:**
```graphql
{
  myActivity {
    id
    action
    details
    createdAt
  }
}
```

### 3. Create Content (Authenticated)

**Create a post:**
```graphql
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    success
    message
    post {
      id
      title
      status
    }
  }
}
```

Variables:
```json
{
  "input": {
    "title": "My GraphQL Journey",
    "content": "Learning GraphQL is fun!",
    "status": "published",
    "canComment": true
  }
}
```

**Create a comment:**
```graphql
mutation CreateComment($input: CommentInput!) {
  createComment(input: $input) {
    success
    message
    comment {
      id
      text
      isApproved
    }
  }
}
```

Variables:
```json
{
  "input": {
    "postId": 1,
    "text": "Great post!"
  }
}
```

### 4. Manage Your Posts

**Update your post:**
```graphql
mutation UpdatePost($id: Int!, $input: PostInput!) {
  updatePost(id: $id, input: $input) {
    success
    post {
      id
      title
      status
    }
  }
}
```

Variables:
```json
{
  "id": 1,
  "input": {
    "title": "Updated Title",
    "content": "Updated content",
    "status": "published"
  }
}
```

**Delete your post:**
```graphql
mutation DeletePost($id: Int!) {
  deletePost(id: $id) {
    success
    message
  }
}
```

Variables:
```json
{
  "id": 1
}
```

### 5. Manage Profile (Authenticated)

**Update profile:**
```graphql
mutation UpdateProfile($input: UserProfileUpdateInput!) {
  updateProfile(input: $input) {
    success
    user {
      firstName
      lastName
      profile {
        bio
      }
    }
  }
}
```

Variables:
```json
{
  "input": {
    "firstName": "Updated",
    "lastName": "Name",
    "bio": "New bio here"
  }
}
```

**Change password:**
```graphql
mutation ChangePassword($input: ChangePasswordInput!) {
  changePassword(input: $input) {
    success
    message
  }
}
```

Variables:
```json
{
  "input": {
    "oldPassword": "TestPass123!",
    "newPassword": "NewPass456!"
  }
}
```

## Admin/Moderator Queries

### For Moderators & Admins

**Get pending comments:**
```graphql
{
  pendingComments {
    id
    text
    authorName
    post {
      title
    }
  }
}
```

**Approve a comment:**
```graphql
mutation ApproveComment($id: Int!) {
  approveComment(id: $id) {
    success
    comment {
      isApproved
    }
  }
}
```

Variables:
```json
{
  "id": 5
}
```

### For Admins Only

**Get all activity:**
```graphql
{
  allActivity {
    id
    username
    action
    details
    createdAt
  }
}
```

**Get user activity:**
```graphql
{
  userActivity(userId: 2) {
    id
    action
    details
    createdAt
  }
}
```

## Sample Users (Created by add_sample_data.py)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| moderator | mod123 | moderator |
| user | user123 | user |

## Permission Levels

### Admin
- ✅ Create/edit/delete own posts
- ✅ Edit/delete ANY post
- ✅ Approve/reject comments
- ✅ View all user activity
- ✅ Manage users

### Moderator
- ✅ Create/edit/delete own posts
- ✅ Approve/reject comments
- ✅ View pending comments
- ✅ Take down offensive posts

### Regular User
- ✅ Create/edit/delete own posts
- ✅ Create comments (need approval)
- ✅ View own activity
- ✅ Cannot see other users' private posts

## How to Use Tokens in Postman

### 1. Get Token from Login
Copy token from login response

### 2. Add to Headers
- Create new header: `Authorization`
- Value: `Bearer <paste_token_here>`

Example:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDAxMjM0NTZ9.abc123...
```

### 3. User is Now Authenticated
All requests with this header will have access to protected queries

## What Happens When...

### Token Expires
- After 24 hours (configurable in settings.py)
- Response: `"Invalid or expired token"`
- Solution: Login again to get new token

### User Tries to Edit Someone Else's Post
- Response: `"You don't have permission to update this post"`
- Solution: Only edit your own posts (or be admin)

### Comment Posted on Closed Post
- Response: `"Comments are disabled for this post"`
- Solution: Author set `can_comment: false`

### Non-Admin Tries Admin Query
- Response: `"Permission denied. Required roles: admin"`
- Solution: Use account with admin role

## Testing with Postman Collection

### Step 1: Import Collection
1. Open Postman
2. Go to Import
3. Select: `postman/GraphQL-App4-Collection.json`

### Step 2: Run Pre-built Requests
- **Register User** - Test user signup
- **Login User** - Get JWT token
- **Get My Posts** - View your posts
- **Create Post** - Write new post
- **Get All Activity** - View all actions (admin)

### Step 3: Add Token to Requests
1. Run login request
2. Copy token from response
3. Edit other requests
4. Add `Authorization: Bearer <token>` header
5. Run authenticated requests

## Key Concepts

### JWT Token (JSON Web Token)
- Encrypted token containing user information
- Sent with every authenticated request
- Automatically expires after set time
- Cannot be modified without the secret key

### Roles (admin, moderator, user)
- Admin: Full access to everything
- Moderator: Can moderate content and approve comments
- User: Can create own content only

### Activity Log
- Records all user actions
- Useful for audits and debugging
- Can be viewed by admins

### Permissions
- **Authentication**: Must be logged in
- **Authorization**: Must have right role
- **Ownership**: Must be the creator or admin

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Authentication credentials not provided" | No Authorization header | Add `Authorization: Bearer <token>` header |
| "Invalid or expired token" | Token expired or invalid | Login again to get new token |
| "User not found" | Token references deleted user | Login again |
| "Permission denied" | Role not high enough | Use higher-privilege account |
| "User already exists" | Username taken | Choose different username |
| "Invalid username or password" | Wrong credentials | Check spelling, case-sensitive |
| "Post not found" | Post ID doesn't exist | Check post ID is valid |

## Database Info

**Database:** SQLite (auto-created)

**Sample Data:**
- 3 users (admin, moderator, user)
- 5 posts (mix of draft/published)
- 8 comments (some pending approval)
- Activity logs from all actions

**Reset database:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py shell < add_sample_data.py
```

## Files to Explore

| File | Purpose |
|------|---------|
| `config/schema.py` | GraphQL schema with all auth logic |
| `auth_app/models.py` | Database models |
| `postman/GraphQL-App4-Collection.json` | 25+ test requests |
| `README.md` | Detailed documentation |

## Next Steps

1. ✅ Run the quick start queries above
2. 📖 Read [README.md](README.md) for detailed explanations
3. 🔍 Explore the schema in `config/schema.py`
4. 💾 Check database relations in `auth_app/models.py`
5. 🧪 Import Postman collection for 25+ real requests
6. 🔐 Build a login page in your frontend

## What You've Learned

✓ JWT token generation and validation  
✓ User registration and authentication  
✓ Role-based access control (RBAC)  
✓ Owner-based permissions for content  
✓ Protected queries and mutations  
✓ Activity logging and audit trails  
✓ Password security and management  
✓ Comment moderation workflow  

## Ready for More?

Check out **App 5** for:
- Performance optimization
- Testing & debugging
- Real-time updates (subscriptions)
- Production deployment

Happy coding! 🚀
