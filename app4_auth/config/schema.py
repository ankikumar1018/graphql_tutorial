import graphene
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from graphene_django import DjangoObjectType
from auth_app.models import UserProfile, Post, Comment, ActivityLog
from django.conf import settings
from functools import wraps


# ==================== JWT Token Management ====================

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(func):
    """Decorator to require authentication"""
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        request = info.context
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            raise Exception('Authentication credentials not provided')
        
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        payload = decode_token(token)
        
        if not payload:
            raise Exception('Invalid or expired token')
        
        # Add user to context
        try:
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except User.DoesNotExist:
            raise Exception('User not found')
        
        return func(self, info, *args, **kwargs)
    return wrapper


def require_role(*allowed_roles):
    """Decorator to check user role"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, *args, **kwargs):
            request = info.context
            
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                raise Exception('Authentication required')
            
            user_role = request.user.profile.role
            
            if user_role not in allowed_roles:
                raise Exception(f'Permission denied. Required roles: {", ".join(allowed_roles)}')
            
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator


# ==================== GraphQL Types ====================

class UserProfileType(DjangoObjectType):
    """User profile with role information"""
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'bio', 'is_email_verified', 'created_at', 'updated_at']


class UserType(DjangoObjectType):
    """User type with profile"""
    profile = graphene.Field(UserProfileType)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
    
    def resolve_profile(self, info):
        return self.profile


class CommentType(DjangoObjectType):
    """Comment type"""
    author_name = graphene.String()
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'is_approved', 'created_at']
    
    def resolve_author_name(self, info):
        return self.author.username


class PostType(DjangoObjectType):
    """Post type with owner and comments"""
    author_name = graphene.String()
    can_edit = graphene.Boolean()
    can_delete = graphene.Boolean()
    comments = graphene.List(CommentType)
    comment_count = graphene.Int()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'status', 'can_comment', 'created_at', 'updated_at']
    
    def resolve_author_name(self, info):
        return self.author.username
    
    def resolve_can_edit(self, info):
        """Check if current user can edit post"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return False
        return self.author.id == request.user.id or request.user.profile.role in ['admin', 'moderator']
    
    def resolve_can_delete(self, info):
        """Check if current user can delete post"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return False
        return self.author.id == request.user.id or request.user.profile.role in ['admin']
    
    def resolve_comments(self, info):
        return self.comments.filter(is_approved=True)
    
    def resolve_comment_count(self, info):
        return self.comments.filter(is_approved=True).count()


class ActivityLogType(DjangoObjectType):
    """Activity log type"""
    username = graphene.String()
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'action', 'details', 'created_at']
    
    def resolve_username(self, info):
        return self.user.username


class TokenType(graphene.ObjectType):
    """JWT Token response"""
    token = graphene.String()
    user = graphene.Field(UserType)
    expires_in = graphene.Int()


# ==================== Input Types ====================

class UserRegisterInput(graphene.InputObjectType):
    """Input for user registration"""
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()


class UserProfileUpdateInput(graphene.InputObjectType):
    """Input for updating user profile"""
    first_name = graphene.String()
    last_name = graphene.String()
    bio = graphene.String()


class ChangePasswordInput(graphene.InputObjectType):
    """Input for changing password"""
    old_password = graphene.String(required=True)
    new_password = graphene.String(required=True)


class PostInput(graphene.InputObjectType):
    """Input for creating/updating posts"""
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    status = graphene.String()
    can_comment = graphene.Boolean()


class CommentInput(graphene.InputObjectType):
    """Input for creating comments"""
    text = graphene.String(required=True)
    post_id = graphene.Int(required=True)


# ==================== Mutations ====================

class Register(graphene.Mutation):
    """Register a new user"""
    class Arguments:
        input = UserRegisterInput(required=True)
    
    user = graphene.Field(UserType)
    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        try:
            # Check if user exists
            if User.objects.filter(username=input.username).exists():
                return Register(success=False, message="Username already exists", user=None, token=None)
            
            if User.objects.filter(email=input.email).exists():
                return Register(success=False, message="Email already exists", user=None, token=None)
            
            # Create user
            user = User.objects.create_user(
                username=input.username,
                email=input.email,
                password=input.password,
                first_name=input.first_name or '',
                last_name=input.last_name or ''
            )
            
            # Generate token
            token = generate_token(user.id)
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='login',
                details='User registration'
            )
            
            return Register(
                success=True,
                message="User registered successfully",
                user=user,
                token=token
            )
        except Exception as e:
            return Register(success=False, message=str(e), user=None, token=None)


class Login(graphene.Mutation):
    """Login user with username and password"""
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserType)
    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    def mutate(root, info, username, password):
        try:
            # Get user
            user = User.objects.filter(username=username).first()
            
            if not user or not check_password(password, user.password):
                return Login(
                    success=False,
                    message="Invalid username or password",
                    user=None,
                    token=None
                )
            
            if not user.is_active:
                return Login(
                    success=False,
                    message="User account is inactive",
                    user=None,
                    token=None
                )
            
            # Generate token
            token = generate_token(user.id)
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='login',
                details='User login successful'
            )
            
            return Login(
                success=True,
                message="Login successful",
                user=user,
                token=token
            )
        except Exception as e:
            return Login(success=False, message=str(e), user=None, token=None)


class UpdateProfile(graphene.Mutation):
    """Update user profile (requires authentication)"""
    class Arguments:
        input = UserProfileUpdateInput(required=True)
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, input):
        try:
            user = info.context.user
            
            # Update user fields
            if input.first_name:
                user.first_name = input.first_name
            if input.last_name:
                user.last_name = input.last_name
            user.save()
            
            # Update profile
            if input.bio:
                user.profile.bio = input.bio
                user.profile.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='update_profile',
                details='Profile updated'
            )
            
            return UpdateProfile(
                success=True,
                message="Profile updated successfully",
                user=user
            )
        except Exception as e:
            return UpdateProfile(success=False, message=str(e), user=None)


class ChangePassword(graphene.Mutation):
    """Change user password (requires authentication)"""
    class Arguments:
        input = ChangePasswordInput(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, input):
        try:
            user = info.context.user
            
            # Verify old password
            if not check_password(input.old_password, user.password):
                return ChangePassword(success=False, message="Old password is incorrect")
            
            # Set new password
            user.set_password(input.new_password)
            user.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='change_password',
                details='Password changed'
            )
            
            return ChangePassword(success=True, message="Password changed successfully")
        except Exception as e:
            return ChangePassword(success=False, message=str(e))


class CreatePost(graphene.Mutation):
    """Create a new post (requires authentication)"""
    class Arguments:
        input = PostInput(required=True)
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, input):
        try:
            user = info.context.user
            
            post = Post.objects.create(
                title=input.title,
                content=input.content,
                author=user,
                status=input.status or 'draft',
                can_comment=input.can_comment if input.can_comment is not None else True
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='create_post',
                details=f'Created post: {post.title}'
            )
            
            return CreatePost(
                success=True,
                message="Post created successfully",
                post=post
            )
        except Exception as e:
            return CreatePost(success=False, message=str(e), post=None)


class UpdatePost(graphene.Mutation):
    """Update a post (owner or admin/moderator only)"""
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, id, input):
        try:
            user = info.context.user
            post = Post.objects.get(id=id)
            
            # Check permission
            if post.author.id != user.id and user.profile.role not in ['admin', 'moderator']:
                return UpdatePost(
                    success=False,
                    message="You don't have permission to update this post",
                    post=None
                )
            
            # Update post
            post.title = input.title
            post.content = input.content
            if input.status:
                post.status = input.status
            if input.can_comment is not None:
                post.can_comment = input.can_comment
            post.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='create_post',
                details=f'Updated post: {post.title}'
            )
            
            return UpdatePost(
                success=True,
                message="Post updated successfully",
                post=post
            )
        except Post.DoesNotExist:
            return UpdatePost(success=False, message="Post not found", post=None)
        except Exception as e:
            return UpdatePost(success=False, message=str(e), post=None)


class DeletePost(graphene.Mutation):
    """Delete a post (owner or admin only)"""
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, id):
        try:
            user = info.context.user
            post = Post.objects.get(id=id)
            
            # Check permission
            if post.author.id != user.id and user.profile.role != 'admin':
                return DeletePost(
                    success=False,
                    message="You don't have permission to delete this post"
                )
            
            post.delete()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='delete_post',
                details=f'Deleted post'
            )
            
            return DeletePost(success=True, message="Post deleted successfully")
        except Post.DoesNotExist:
            return DeletePost(success=False, message="Post not found")
        except Exception as e:
            return DeletePost(success=False, message=str(e))


class CreateComment(graphene.Mutation):
    """Create a comment on a post (requires authentication)"""
    class Arguments:
        input = CommentInput(required=True)
    
    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    def mutate(root, info, input):
        try:
            user = info.context.user
            post = Post.objects.get(id=input.post_id)
            
            if not post.can_comment:
                return CreateComment(
                    success=False,
                    message="Comments are disabled for this post",
                    comment=None
                )
            
            comment = Comment.objects.create(
                text=input.text,
                author=user,
                post=post,
                is_approved=user.profile.role in ['admin', 'moderator']  # Auto-approve for moderators
            )
            
            return CreateComment(
                success=True,
                message="Comment created successfully",
                comment=comment
            )
        except Post.DoesNotExist:
            return CreateComment(success=False, message="Post not found", comment=None)
        except Exception as e:
            return CreateComment(success=False, message=str(e), comment=None)


class ApproveComment(graphene.Mutation):
    """Approve a comment (moderator/admin only)"""
    class Arguments:
        id = graphene.Int(required=True)
    
    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    message = graphene.String()
    
    @staticmethod
    @require_auth
    @require_role('admin', 'moderator')
    def mutate(root, info, id):
        try:
            comment = Comment.objects.get(id=id)
            comment.is_approved = True
            comment.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=info.context.user,
                action='update_profile',
                details=f'Approved comment'
            )
            
            return ApproveComment(
                success=True,
                message="Comment approved",
                comment=comment
            )
        except Comment.DoesNotExist:
            return ApproveComment(success=False, message="Comment not found", comment=None)
        except Exception as e:
            return ApproveComment(success=False, message=str(e), comment=None)


class Mutation(graphene.ObjectType):
    """All mutations"""
    register = Register.Field()
    login = Login.Field()
    update_profile = UpdateProfile.Field()
    change_password = ChangePassword.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    approve_comment = ApproveComment.Field()


# ==================== Queries ====================

class Query(graphene.ObjectType):
    """All queries"""
    
    # User queries
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    all_users = graphene.List(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    
    # Post queries
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    all_posts = graphene.List(PostType)
    my_posts = graphene.List(PostType)
    user_posts = graphene.List(PostType, user_id=graphene.Int(required=True))
    published_posts = graphene.List(PostType)
    
    # Comment queries
    post_comments = graphene.List(CommentType, post_id=graphene.Int(required=True))
    pending_comments = graphene.List(CommentType)
    
    # Activity queries
    my_activity = graphene.List(ActivityLogType)
    user_activity = graphene.List(ActivityLogType, user_id=graphene.Int(required=True))
    all_activity = graphene.List(ActivityLogType)
    
    def resolve_me(self, info):
        """Get current authenticated user"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return None
        return request.user
    
    def resolve_user(self, info, id):
        """Get user by ID"""
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    
    def resolve_all_users(self, info):
        """Get all users"""
        return User.objects.filter(is_active=True)
    
    def resolve_user_by_username(self, info, username):
        """Get user by username"""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    def resolve_post(self, info, id):
        """Get post by ID"""
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None
    
    def resolve_all_posts(self, info):
        """Get all published posts"""
        return Post.objects.filter(status='published')
    
    def resolve_my_posts(self, info):
        """Get current user's posts (requires auth)"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=request.user)
    
    def resolve_user_posts(self, info, user_id):
        """Get posts by specific user"""
        return Post.objects.filter(author_id=user_id, status='published')
    
    def resolve_published_posts(self, info):
        """Get all published posts (paginated)"""
        return Post.objects.filter(status='published')
    
    def resolve_post_comments(self, info, post_id):
        """Get comments for a post"""
        try:
            post = Post.objects.get(id=post_id)
            return post.comments.filter(is_approved=True)
        except Post.DoesNotExist:
            return Comment.objects.none()
    
    def resolve_pending_comments(self, info):
        """Get pending comments (admin/moderator only)"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return Comment.objects.none()
        
        if request.user.profile.role not in ['admin', 'moderator']:
            return Comment.objects.none()
        
        return Comment.objects.filter(is_approved=False)
    
    def resolve_my_activity(self, info):
        """Get current user's activity (requires auth)"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return ActivityLog.objects.none()
        return ActivityLog.objects.filter(user=request.user)[:20]
    
    def resolve_user_activity(self, info, user_id):
        """Get user activity (admin only)"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return ActivityLog.objects.none()
        
        if request.user.profile.role != 'admin':
            return ActivityLog.objects.none()
        
        return ActivityLog.objects.filter(user_id=user_id)[:20]
    
    def resolve_all_activity(self, info):
        """Get all activity (admin only)"""
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return ActivityLog.objects.none()
        
        if request.user.profile.role != 'admin':
            return ActivityLog.objects.none()
        
        return ActivityLog.objects.all()[:100]


schema = graphene.Schema(query=Query, mutation=Mutation)
