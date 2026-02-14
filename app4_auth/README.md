# App 4: Authentication, Authorization & Permissions

Learn JWT-based authentication, role-based access control (RBAC), and permission-based query patterns.

## What You'll Learn

### Core Topics
- **JWT Authentication**: Token generation, validation, and expiration handling
- **User Registration & Login**: Create accounts and authenticate users
- **Role-Based Access Control (RBAC)**: Restrict queries/mutations by user role (admin, moderator, user)
- **Owner-Based Permissions**: Let users edit/delete only their own content
- **Protected Queries**: Authentication requirements on sensitive operations
- **Activity Logging**: Track user actions for audit trails
- **Password Security**: Hashing, validation, and change operations

### Key Patterns Covered
1. **Token Generation**: JWT tokens with expiration
2. **Token Validation**: Decode and verify tokens on protected endpoints
3. **Authentication Decorators**: Reusable function decorators for auth checks
4. **Role Checking**: Verify user roles before allowing actions
5. **Ownership Verification**: Allow owner + admins to edit/delete
6. **Activity Tracking**: Automatically log user actions
7. **Registration & Login**: Complete user lifecycle

## Project Structure

```
app4_auth/
├── config/
│   ├── settings.py          # Django settings (JWT config)
│   ├── urls.py              # GraphQL endpoint
│   ├── schema.py            # GraphQL schema with auth
│   └── __init__.py
├── auth_app/
│   ├── models.py            # User, Post, Comment, ActivityLog models
│   ├── admin.py             # Django admin setup
│   ├── apps.py
│   └── migrations/
├── postman/
│   └── GraphQL-App4-Collection.json  # 25+ test requests
├── manage.py
├── requirements.txt
├── add_sample_data.py       # Create sample users & posts
├── README.md                # This file
├── QUICKSTART.md            # Quick start guide
└── .gitignore
```

## Data Models

### UserProfile Model
```python
class UserProfile(models.Model):
    user = OneToOneField(User)
    role = CharField(choices=['admin', 'moderator', 'user'])
    bio = TextField()
    is_email_verified = BooleanField(default=False)
```

### Post Model
```python
class Post(models.Model):
    title = CharField()
    content = TextField()
    author = ForeignKey(User)
    status = CharField(choices=['draft', 'published', 'archived'])
    can_comment = BooleanField()
```

### Comment Model
```python
class Comment(models.Model):
    text = TextField()
    post = ForeignKey(Post)
    author = ForeignKey(User)
    is_approved = BooleanField()
```

### ActivityLog Model
```python
class ActivityLog(models.Model):
    user = ForeignKey(User)
    action = CharField()  # login, logout, create_post, etc
    details = TextField()
    ip_address = GenericIPAddressField()
```

## JWT Token Structure

### Token Generation
```python
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
    return token
```

### Using Tokens in Requests

Include token in `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

Example:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDAxMjM0NTYsImlhdCI6MTU5OTUyNDQ1Nn0.DZ6HwFVFyDk9Z3C3P4Y1K0X8Q2B5N6M7J...
```

## GraphQL Schema Overview

### Mutations (11 total)

#### Authentication Mutations
```graphql
register(input: UserRegisterInput!): RegisterPayload
login(username: String!, password: String!): LoginPayload
```

#### Profile Mutations
```graphql
updateProfile(input: UserProfileUpdateInput!): UpdateProfilePayload
changePassword(input: ChangePasswordInput!): ChangePasswordPayload
```

#### Post Mutations
```graphql
createPost(input: PostInput!): CreatePostPayload
updatePost(id: Int!, input: PostInput!): UpdatePostPayload
deletePost(id: Int!): DeletePostPayload
```

#### Comment Mutations
```graphql
createComment(input: CommentInput!): CreateCommentPayload
approveComment(id: Int!): ApproveCommentPayload  # Moderator/Admin only
```

### Queries (13 total)

#### User Queries
```graphql
me: User                                    # Current authenticated user
user(id: Int!): User                       # Get user by ID
allUsers: [User]                           # All active users
userByUsername(username: String!): User    # Get user by username
```

#### Post Queries
```graphql
post(id: Int!): Post                       # Get post by ID
allPosts: [Post]                           # All published posts
myPosts: [Post]                            # Current user's posts (auth required)
userPosts(userId: Int!): [Post]            # All posts by user
publishedPosts: [Post]                     # All published posts (paginated)
```

#### Comment Queries
```graphql
postComments(postId: Int!): [Comment]      # Comments for post
pendingComments: [Comment]                 # Unapproved comments (moderator only)
```

#### Activity Queries
```graphql
myActivity: [ActivityLog]                  # Current user's activity (auth required)
userActivity(userId: Int!): [ActivityLog]  # User activity (admin only)
allActivity: [ActivityLog]                 # All activity (admin only)
```

## GraphQL Query Examples

### 1. Registration & Login

**Register new user:**
```graphql
mutation RegisterUser($input: UserRegisterInput!) {
  register(input: $input) {
    success
    message
    user {
      id
      username
      email
    }
    token
  }
}
```

Variables:
```json
{
  "input": {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

**Login user:**
```graphql
mutation LoginUser($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    success
    message
    user {
      id
      username
      profile {
        role
      }
    }
    token
  }
}
```

Variables:
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

Response:
```json
{
  "data": {
    "login": {
      "success": true,
      "message": "Login successful",
      "user": {
        "id": "123",
        "username": "john_doe",
        "profile": {
          "role": "user"
        }
      },
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
}
```

### 2. Protected Queries (Requires Authentication)

**Get current authenticated user:**
```graphql
{
  me {
    id
    username
    email
    firstName
    lastName
    profile {
      role
      bio
      isEmailVerified
    }
  }
}
```

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Get my posts (authenticated):**
```graphql
{
  myPosts {
    id
    title
    content
    status
    createdAt
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

### 3. Public Queries (No Authentication)

**Get all published posts:**
```graphql
{
  allPosts {
    id
    title
    authorName
    status
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
    canComment
    comments {
      id
      text
      authorName
      createdAt
    }
    commentCount
  }
}
```

**Get user profile:**
```graphql
{
  userByUsername(username: "john_doe") {
    id
    username
    profile {
      bio
      role
    }
  }
}
```

### 4. Profile Management (Authenticated)

**Update profile:**
```graphql
mutation UpdateProfile($input: UserProfileUpdateInput!) {
  updateProfile(input: $input) {
    success
    message
    user {
      id
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
    "firstName": "John",
    "lastName": "Updated",
    "bio": "I love GraphQL and Django!"
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
    "oldPassword": "OldPass123!",
    "newPassword": "NewPass456!"
  }
}
```

### 5. Create & Manage Posts (Authenticated)

**Create a new post:**
```graphql
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    success
    message
    post {
      id
      title
      status
      authorName
      createdAt
    }
  }
}
```

Variables:
```json
{
  "input": {
    "title": "My First GraphQL Post",
    "content": "GraphQL is amazing! Here's why...",
    "status": "published",
    "canComment": true
  }
}
```

**Create draft post:**
```graphql
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    success
    post {
      id
      status
    }
  }
}
```

Variables:
```json
{
  "input": {
    "title": "Work in Progress",
    "content": "I'll finish this later",
    "status": "draft"
  }
}
```

**Update own post:**
```graphql
mutation UpdatePost($id: Int!, $input: PostInput!) {
  updatePost(id: $id, input: $input) {
    success
    message
    post {
      id
      title
      content
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

**Delete own post:**
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

### 6. Comments (Authenticated)

**Create comment on post:**
```graphql
mutation CreateComment($input: CommentInput!) {
  createComment(input: $input) {
    success
    message
    comment {
      id
      text
      authorName
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
    "text": "Great post! Really helpful."
  }
}
```

**Get comments for post:**
```graphql
{
  postComments(postId: 1) {
    id
    text
    authorName
    isApproved
    createdAt
  }
}
```

### 7. Moderation - Approve Comments (Moderator/Admin Only)

**Get pending comments (moderator):**
```graphql
{
  pendingComments {
    id
    text
    authorName
    post {
      title
    }
    createdAt
  }
}
```

**Approve comment:**
```graphql
mutation ApproveComment($id: Int!) {
  approveComment(id: $id) {
    success
    message
    comment {
      id
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

### 8. Admin Queries - Activity Logs

**Get all user activity (admin):**
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

Possible actions: `login`, `logout`, `create_post`, `delete_post`, `update_profile`, `change_password`

**Get specific user's activity (admin):**
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

### 9. Permission Check Examples

**Check if I can edit post:**
```graphql
{
  post(id: 1) {
    id
    title
    canEdit      # true if you're the author or admin/moderator
    canDelete    # true if you're the author or admin
  }
}
```

**Try to edit another user's post (fails):**
```graphql
mutation UpdatePost($id: Int!, $input: PostInput!) {
  updatePost(id: $id, input: $input) {
    success
    message  # "You don't have permission to update this post"
  }
}
```

Variables:
```json
{
  "id": 999,
  "input": {
    "title": "Hacked",
    "content": "Hacked"
  }
}
```

## Role-Based Access Control (RBAC)

### Three Role Levels

| Role | Capabilities |
|------|--------------|
| **admin** | • Create/edit/delete own posts<br>• Edit/delete any post<br>• Approve comments<br>• View all activity<br>• View all users |
| **moderator** | • Create/edit/delete own posts<br>• Approve/reject comments<br>• View pending comments |
| **user** | • Create/edit/delete own posts<br>• Create comments (needs approval)<br>• View own activity |

### Permission Checking

All protected mutations check authentication:
```python
@require_auth
def mutate(root, info, ...):
    user = info.context.user
    # User is authenticated
```

Some mutations check role:
```python
@require_auth
@require_role('admin', 'moderator')
def mutate(root, info, ...):
    # Only admin/moderator can access
```

Owner-based permissions:
```python
if post.author.id != user.id and user.profile.role not in ['admin', 'moderator']:
    raise Exception("Permission denied")
```

## Authentication Flow

### Step 1: User Registers
```
Client → Register mutation with credentials
↓
Server → Creates User + UserProfile (role='user')
↓
Server → Returns JWT token
↓
Client → Stores token (localStorage, sessionStorage, etc)
```

### Step 2: User Logs In
```
Client → Login mutation with username/password
↓
Server → Validates credentials
↓
Server → Generates JWT token
↓
Client → Stores token
```

### Step 3: Make Authenticated Request
```
Client → Sends query/mutation with Authorization header
↓
Server → Decodes token from header
↓
Server → Validates token signature & expiration
↓
Server → Attaches user to request context
↓
Server → Executes query/mutation
```

### Step 4: Token Expiration
```
Token valid for: 24 hours (configurable)
↓
After expiration: User must login again to get new token
↓
Expired token response: "Invalid or expired token"
```

## Security Features

### Password Security
- Passwords hashed using PBKDF2 (Django's default)
- Password validation on registration
- Change password requires old password verification

### JWT Security
- Signed with secret key
- Includes expiration timestamp
- Verified on every protected request
- Bearer token format (industry standard)

### Activity Logging
- All actions logged: login, create_post, delete_post, etc
- Tracks user, action, details, timestamp
- IP address stored for audit trails

### Authorization Checks
```python
# Authentication required
@require_auth

# Role-based access
@require_role('admin', 'moderator')

# Owner-based access
if post.author != current_user and current_user.role != 'admin':
    raise Exception("Not allowed")
```

## Common Patterns

### Pattern 1: Authenticate User

**In React/JavaScript:**
```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/graphql/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    query: '{ me { id username } }'
  })
});
```

### Pattern 2: Check if User is Admin

**In GraphQL query:**
```graphql
{
  me {
    profile {
      role
    }
  }
}
```

**In client code:**
```javascript
if (user.profile.role === 'admin') {
  // Show admin panel
}
```

### Pattern 3: Handle Token Expiration

**When token expires (401 error):**
```javascript
if (error.status === 401 || error.message.includes('expired')) {
  // Redirect to login
  window.location.href = '/login';
  localStorage.removeItem('token');
}
```

## Troubleshooting

### Issue: "Authentication credentials not provided"
**Solution:** Include `Authorization: Bearer <token>` header in request

### Issue: "Invalid or expired token"
**Solution:** Token expired after 24 hours. Login again to get new token.

### Issue: "User not found"
**Solution:** Token references deleted user. Delete token and login again.

### Issue: "Permission denied"
**Solution:** Your role doesn't have permission. Check required role for the operation.

### Issue: "Username already exists"
**Solution:** Choose a different username during registration.

### Issue: "Invalid username or password"
**Solution:** Check credentials are correct. Username/email is case-sensitive.

## Installation & Setup

See [QUICKSTART.md](QUICKSTART.md) for step-by-step setup instructions.

## API Testing

Use the included Postman collection:
- **File:** `postman/GraphQL-App4-Collection.json`
- **Requests:** 25+ pre-built auth, RBAC, and permission examples
- **Import:** Postman → Import → Select the JSON file

## What's Next?

After mastering App 4, explore:
- **App 5:** Performance & Real-time

---

**Created:** 2024  
**Updated:** 2024
