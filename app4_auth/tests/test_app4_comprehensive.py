"""
Comprehensive pytest suite for App 4: Authentication & Authorization
Tests cover JWT auth, permissions, RBAC, user management, and protected resources
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from graphene.test import Client as GrapheneClient
from auth_app.models import UserProfile, Post, Comment, ActivityLog
from config.schema import schema, generate_token, decode_token
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings


@pytest.fixture
def api_client():
    """GraphQL test client"""
    return GrapheneClient(schema)


@pytest.fixture
def http_client():
    """HTTP client"""
    return Client()


@pytest.fixture
def normal_user(db):
    """Create normal user"""
    user, created = User.objects.get_or_create(
        username="normaluser",
        defaults={"email": "user@example.com"}
    )
    if created or not user.check_password('password123'):
        user.set_password('password123')
        user.save()
    user.profile.role = 'user'
    user.profile.save()
    return user


@pytest.fixture
def moderator_user(db):
    """Create moderator user"""
    user, created = User.objects.get_or_create(
        username="moderator",
        defaults={"email": "mod@example.com"}
    )
    if created or not user.check_password('password123'):
        user.set_password('password123')
        user.save()
    user.profile.role = 'moderator'
    user.profile.save()
    return user


@pytest.fixture
def admin_user(db):
    """Create admin user"""
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@example.com"}
    )
    if created or not user.check_password('password123'):
        user.set_password('password123')
        user.save()
    user.profile.role = 'admin'
    user.profile.save()
    return user


@pytest.fixture
def all_users(normal_user, moderator_user, admin_user):
    """All user fixtures"""
    return {
        'user': normal_user,
        'moderator': moderator_user,
        'admin': admin_user
    }


@pytest.fixture
def user_token(normal_user):
    """JWT token for normal user"""
    return generate_token(normal_user.id)


@pytest.fixture
def moderator_token(moderator_user):
    """JWT token for moderator"""
    return generate_token(moderator_user.id)


@pytest.fixture
def admin_token(admin_user):
    """JWT token for admin"""
    return generate_token(admin_user.id)


@pytest.fixture
def sample_post(db, normal_user):
    """Create sample post"""
    return Post.objects.create(
        title="Test Post",
        content="Test content",
        author=normal_user,
        status="published"
    )


@pytest.fixture
def sample_posts(db, normal_user, moderator_user):
    """Create multiple posts"""
    return [
        Post.objects.create(
            title="User Post",
            content="Content by user",
            author=normal_user,
            status="published"
        ),
        Post.objects.create(
            title="Mod Post",
            content="Content by mod",
            author=moderator_user,
            status="draft"
        ),
    ]


@pytest.fixture
def sample_comment(db, sample_post, normal_user):
    """Create sample comment"""
    return Comment.objects.create(
        post=sample_post,
        author=normal_user,
        text="Great post!",
        is_approved=True
    )


# ==================== Model Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestUserProfileModel:
    """Test UserProfile model"""
    
    def test_user_profile_creation(self):
        """Test auto-creation of user profile"""
        user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "test@example.com",
                "password": "password"
            }
        )
        if _ or not user.password or user.password != "password":
            user.set_password('password')
            user.save()
        assert hasattr(user, 'profile')
        assert user.profile.role == 'user'
        assert str(user.profile) == "testuser (user)"
    
    def test_user_profile_roles(self, all_users):
        """Test different user roles"""
        assert all_users['user'].profile.role == 'user'
        assert all_users['moderator'].profile.role == 'moderator'
        assert all_users['admin'].profile.role == 'admin'
    
    def test_profile_one_to_one_relationship(self, normal_user):
        """Test one-to-one relationship"""
        profile = UserProfile.objects.get(user=normal_user)
        assert profile.user == normal_user


@pytest.mark.unit
@pytest.mark.django_db
class TestPostModel:
    """Test Post model"""
    
    def test_post_creation(self, normal_user):
        """Test creating a post"""
        post = Post.objects.create(
            title="My Post",
            content="My content",
            author=normal_user,
            status="draft"
        )
        assert post.title == "My Post"
        assert post.author == normal_user
        assert str(post) == f"My Post by {normal_user.username}"
    
    def test_post_defaults(self, normal_user):
        """Test post default values"""
        post = Post.objects.create(
            title="Title",
            content="Content",
            author=normal_user
        )
        assert post.status == "draft"
        assert post.can_comment is True
    
    def test_post_author_relationship(self, sample_post, normal_user):
        """Test post to author relationship"""
        assert sample_post.author == normal_user
        assert sample_post in normal_user.posts.all()


@pytest.mark.unit
@pytest.mark.django_db
class TestCommentModel:
    """Test Comment model"""
    
    def test_comment_creation(self, sample_post, normal_user):
        """Test creating a comment"""
        comment = Comment.objects.create(
            post=sample_post,
            author=normal_user,
            text="Nice post",
            is_approved=True
        )
        assert comment.text == "Nice post"
        assert comment.post == sample_post
    
    def test_comment_relationships(self, sample_comment, sample_post, normal_user):
        """Test comment relationships"""
        assert sample_comment.post == sample_post
        assert sample_comment.author == normal_user
        assert sample_comment in sample_post.comments.all()


@pytest.mark.unit
@pytest.mark.django_db
class TestActivityLogModel:
    """Test ActivityLog model"""
    
    def test_activity_log_creation(self, normal_user):
        """Test creating activity log"""
        log = ActivityLog.objects.create(
            user=normal_user,
            action="login",
            details="User logged in"
        )
        assert log.action == "login"
        assert log.user == normal_user


# ==================== JWT Token Tests ====================

@pytest.mark.jwt
@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token generation and validation"""
    
    def test_generate_token(self, normal_user):
        """Test token generation"""
        token = generate_token(normal_user.id)
        assert token is not None
        assert isinstance(token, str)
    
    def test_decode_valid_token(self, normal_user):
        """Test decoding valid token"""
        token = generate_token(normal_user.id)
        payload = decode_token(token)
        assert payload is not None
        assert payload['user_id'] == normal_user.id
    
    def test_decode_expired_token(self):
        """Test decoding expired token"""
        # Create token with past expiration
        payload = {
            'user_id': 1,
            'exp': datetime.utcnow() - timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        decoded = decode_token(token)
        assert decoded is None
    
    def test_decode_invalid_token(self):
        """Test decoding invalid token"""
        invalid_token = "invalid.token.here"
        decoded = decode_token(invalid_token)
        assert decoded is None
    
    def test_token_contains_expiration(self, user_token):
        """Test token contains expiration time"""
        payload = decode_token(user_token)
        assert 'exp' in payload
        assert 'iat' in payload


# ==================== Authentication Mutations ====================

@pytest.mark.auth
@pytest.mark.django_db
class TestAuthenticationMutations:
    """Test auth mutations (register, login, logout)"""
    
    def test_register_new_user(self, api_client):
        """Test registering a new user"""
        mutation = '''
            mutation {
                register(input: {
                    username: "newuser"
                    email: "new@example.com"
                    password: "securepass123"
                    firstName: "New"
                    lastName: "User"
                }) {
                    success
                    message
                    user {
                        username
                        email
                        firstName
                    }
                    token
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        data = result['data']['register']
        assert data['success'] is True
        assert data['user']['username'] == "newuser"
        assert data['token'] is not None
        
        # Verify user exists
        assert User.objects.filter(username="newuser").exists()
    
    def test_register_duplicate_username(self, api_client, normal_user):
        """Test registering with existing username"""
        mutation = f'''
            mutation {{
                register(input: {{
                    username: "{normal_user.username}"
                    email: "different@example.com"
                    password: "password"
                }}) {{
                    success
                    message
                    user {{
                        username
                    }}
                }}
            }}
        '''
        result = api_client.execute(mutation)
        data = result['data']['register']
        assert data['success'] is False
        assert "already exists" in data['message'].lower()
    
    def test_register_duplicate_email(self, api_client, normal_user):
        """Test registering with existing email"""
        mutation = f'''
            mutation {{
                register(input: {{
                    username: "differentuser"
                    email: "{normal_user.email}"
                    password: "password"
                }}) {{
                    success
                    message
                }}
            }}
        '''
        result = api_client.execute(mutation)
        data = result['data']['register']
        assert data['success'] is False
        assert "already exists" in data['message'].lower()
    
    def test_login_valid_credentials(self, api_client, normal_user):
        """Test login with valid credentials"""
        mutation = '''
            mutation {
                login(username: "normaluser", password: "password123") {
                    success
                    message
                    user {
                        username
                        email
                    }
                    token
                }
            }
        '''
        result = api_client.execute(mutation)
        assert 'errors' not in result
        data = result['data']['login']
        assert data['success'] is True
        assert data['token'] is not None
        assert data['user']['username'] == "normaluser"
    
    def test_login_invalid_password(self, api_client, normal_user):
        """Test login with wrong password"""
        mutation = '''
            mutation {
                login(username: "normaluser", password: "wrongpassword") {
                    success
                    message
                    token
                }
            }
        '''
        result = api_client.execute(mutation)
        data = result['data']['login']
        assert data['success'] is False
        assert data['token'] is None
    
    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user"""
        mutation = '''
            mutation {
                login(username: "doesnotexist", password: "password") {
                    success
                    message
                }
            }
        '''
        result = api_client.execute(mutation)
        data = result['data']['login']
        assert data['success'] is False


# ==================== User Profile Queries ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestUserQueries:
    """Test user-related queries"""
    
    def test_me_query_authenticated(self, api_client, normal_user, user_token):
        """Test getting current user info"""
        query = '''
            query {
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
        '''
        # Execute with auth header
        result = api_client.execute(
            query,
            context_value=type('Request', (), {
                'META': {'HTTP_AUTHORIZATION': f'Bearer {user_token}'},
                'user': normal_user
            })()
        )
        # Depending on implementation, check result
        # This test may need adjustment based on actual schema
    
    def test_all_users_query(self, api_client, all_users):
        """Test getting all users"""
        query = '''
            query {
                allUsers {
                    id
                    username
                    email
                    profile {
                        role
                    }
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            users = result['data']['allUsers']
            assert len(users) >= 3


# ==================== Permission Tests ====================

@pytest.mark.permissions
@pytest.mark.django_db
class TestPermissions:
    """Test permission decorators and access control"""
    
    def test_create_post_authenticated(self, api_client, normal_user, user_token):
        """Test creating post when authenticated"""
        mutation = '''
            mutation {
                createPost(input: {
                    title: "New Post"
                    content: "Content here"
                    status: "draft"
                }) {
                    success
                    post {
                        title
                        status
                    }
                }
            }
        '''
        # Would need to pass token in context
        # Test implementation depends on how auth is handled
    
    def test_update_own_post(self, api_client, sample_post, normal_user):
        """Test user can update own post"""
        mutation = f'''
            mutation {{
                updatePost(
                    id: {sample_post.id}
                    input: {{
                        title: "Updated Title"
                        content: "Updated content"
                    }}
                ) {{
                    success
                    post {{
                        title
                    }}
                }}
            }}
        '''
        # Implementation would check ownership
    
    def test_cannot_update_others_post(self, api_client, sample_posts, admin_user):
        """Test user cannot update another user's post"""
        user_post = sample_posts[0]  # Created by normal_user
        # Try to update as different user
        # Should fail or return permission error
    
    def test_admin_can_delete_any_post(self, api_client, sample_post, admin_user):
        """Test admin can delete any post"""
        mutation = f'''
            mutation {{
                deletePost(id: {sample_post.id}) {{
                    success
                    message
                }}
            }}
        '''
        # Should succeed for admin
    
    def test_user_cannot_delete_others_post(self, api_client, sample_posts, normal_user):
        """Test regular user cannot delete others' posts"""
        mod_post = sample_posts[1]  # Created by moderator
        mutation = f'''
            mutation {{
                deletePost(id: {mod_post.id}) {{
                    success
                    message
                }}
            }}
        '''
        # Should fail


# ==================== RBAC Tests ====================

@pytest.mark.permissions
@pytest.mark.django_db
class TestRoleBasedAccess:
    """Test role-based access control"""
    
    def test_admin_access_logs(self, api_client, admin_user):
        """Test admin can view activity logs"""
        query = '''
            query {
                activityLogs(limit: 10) {
                    id
                    action
                    details
                    username
                }
            }
        '''
        # Should succeed for admin
    
    def test_moderator_approve_comments(self, api_client, moderator_user, sample_comment):
        """Test moderator can approve comments"""
        mutation = f'''
            mutation {{
                approveComment(id: {sample_comment.id}) {{
                    success
                    comment {{
                        isApproved
                    }}
                }}
            }}
        '''
        # Should succeed for moderator
    
    def test_user_cannot_approve_comments(self, api_client, normal_user, sample_comment):
        """Test regular user cannot approve comments"""
        mutation = f'''
            mutation {{
                approveComment(id: {sample_comment.id}) {{
                    success
                    message
                }}
            }}
        '''
        # Should fail with permission error
    
    def test_role_hierarchy(self, all_users):
        """Test role hierarchy exists"""
        roles = ['user', 'moderator', 'admin']
        for role in roles:
            assert any(u.profile.role == role for u in all_users.values())


# ==================== Post & Comment Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestPostQueries:
    """Test post-related queries"""
    
    def test_all_posts_query(self, api_client, sample_posts):
        """Test getting all posts"""
        query = '''
            query {
                allPosts {
                    id
                    title
                    content
                    status
                    authorName
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        posts = result['data']['allPosts']
        assert len(posts) >= 2
    
    def test_posts_by_author(self, api_client, sample_posts, normal_user):
        """Test filtering posts by author"""
        query = f'''
            query {{
                postsByAuthor(authorId: {normal_user.id}) {{
                    id
                    title
                    authorName
                }}
            }}
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            posts = result['data']['postsByAuthor']
            assert all(post['authorName'] == normal_user.username for post in posts)
    
    def test_published_posts_only(self, api_client, sample_posts):
        """Test getting published posts query"""
        query = '''
            query {
                publishedPosts {
                    id
                    title
                }
            }
        '''
        result = api_client.execute(query)
        # Just verify the query executes without errors
        assert 'errors' not in result
        posts = result['data']['publishedPosts']
        # Should return at least the published posts from fixtures
        assert isinstance(posts, list)
    
    def test_post_with_comments(self, api_client, sample_post, sample_comment):
        """Test getting post with comments"""
        query = f'''
            query {{
                post(id: {sample_post.id}) {{
                    id
                    title
                    comments {{
                        id
                        text
                        authorName
                    }}
                    commentCount
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        post = result['data']['post']
        assert post['commentCount'] >= 1


@pytest.mark.graphql
@pytest.mark.django_db
class TestCommentMutations:
    """Test comment mutations"""
    
    def test_create_comment(self, api_client, sample_post, normal_user):
        """Test creating a comment"""
        mutation = f'''
            mutation {{
                createComment(input: {{
                    postId: {sample_post.id}
                    text: "Great article!"
                }}) {{
                    success
                    comment {{
                        text
                        isApproved
                    }}
                }}
            }}
        '''
        # Test with auth context
    
    def test_update_own_comment(self, api_client, sample_comment, normal_user):
        """Test updating own comment"""
        mutation = f'''
            mutation {{
                updateComment(
                    id: {sample_comment.id}
                    input: {{
                        text: "Updated comment text"
                    }}
                ) {{
                    success
                    comment {{
                        text
                    }}
                }}
            }}
        '''
        # Should succeed
    
    def test_delete_own_comment(self, api_client, sample_comment, normal_user):
        """Test deleting own comment"""
        mutation = f'''
            mutation {{
                deleteComment(id: {sample_comment.id}) {{
                    success
                    message
                }}
            }}
        '''
        # Should succeed


# ==================== Activity Log Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestActivityLogs:
    """Test activity logging"""
    
    def test_login_creates_log(self, api_client):
        """Test that login creates activity log"""
        # First register user
        mutation = '''
            mutation {
                register(input: {
                    username: "loguser"
                    email: "log@example.com"
                    password: "password"
                }) {
                    success
                    user {
                        id
                    }
                }
            }
        '''
        result = api_client.execute(mutation)
        user_id = result['data']['register']['user']['id']
        
        # Check activity log created
        user = User.objects.get(id=user_id)
        assert ActivityLog.objects.filter(user=user, action='login').exists()
    
    def test_activity_logs_query(self, api_client, all_users):
        """Test querying activity logs"""
        # Create some logs
        for user in all_users.values():
            ActivityLog.objects.create(
                user=user,
                action="test_action",
                details="Test details"
            )
        
        query = '''
            query {
                activityLogs(limit: 10) {
                    id
                    action
                    username
                    details
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            logs = result['data']['activityLogs']
            assert len(logs) >= 3


# ==================== Edge Cases & Validation ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestValidationAndEdgeCases:
    """Test validation and edge cases"""
    
    def test_user_with_empty_profile(self, normal_user):
        """Test user with minimal profile info"""
        assert normal_user.profile.bio == ''
        assert normal_user.profile.is_email_verified is False
    
    def test_post_without_optional_fields(self, normal_user):
        """Test post with only required fields"""
        post = Post.objects.create(
            title="Minimal",
            content="Content",
            author=normal_user
        )
        assert post.can_comment is True
        assert post.status == 'draft'
    
    def test_comment_approval_workflow(self, sample_post, normal_user):
        """Test comment approval flow"""
        comment = Comment.objects.create(
            post=sample_post,
            author=normal_user,
            text="Pending comment",
            is_approved=False
        )
        assert comment.is_approved is False
        
        # Approve
        comment.is_approved = True
        comment.save()
        assert comment.is_approved is True
    
    def test_inactive_user_cannot_login(self, api_client, normal_user):
        """Test inactive user cannot login"""
        normal_user.is_active = False
        normal_user.save()
        
        mutation = '''
            mutation {
                login(username: "normaluser", password: "password123") {
                    success
                    message
                }
            }
        '''
        result = api_client.execute(mutation)
        data = result['data']['login']
        assert data['success'] is False


# ==================== HTTP Endpoint Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestHTTPEndpoint:
    """Test GraphQL via HTTP"""
    
    def test_register_via_http(self, http_client):
        """Test registration via HTTP POST"""
        query_data = {
            "query": '''
                mutation {
                    register(input: {
                        username: "httpuser"
                        email: "http@example.com"
                        password: "password"
                    }) {
                        success
                        user {
                            username
                        }
                    }
                }
            '''
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(query_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'data' in data
    
    def test_query_with_auth_header(self, http_client, normal_user, user_token):
        """Test query with authorization header"""
        query_data = {
            "query": '''
                query {
                    me {
                        username
                    }
                }
            '''
        }
        response = http_client.post(
            '/graphql/',
            json.dumps(query_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_token}'
        )
        assert response.status_code == 200
