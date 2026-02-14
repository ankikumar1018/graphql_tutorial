"""
Script to populate App 4 with sample data including users, posts, and comments.

Run this after migrations:
python manage.py shell < add_sample_data.py
"""

import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from auth_app.models import UserProfile, Post, Comment, ActivityLog

# Clear existing data
Comment.objects.all().delete()
Post.objects.all().delete()
User.objects.all().delete()

print("Creating users...")

# Create admin user
admin_user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='admin123',
    first_name='Admin',
    last_name='User'
)
admin_profile = admin_user.profile
admin_profile.role = 'admin'
admin_profile.bio = 'I am the administrator'
admin_profile.is_email_verified = True
admin_profile.save()

# Create moderator user
moderator_user = User.objects.create_user(
    username='moderator',
    email='moderator@example.com',
    password='mod123',
    first_name='Mod',
    last_name='User'
)
moderator_profile = moderator_user.profile
moderator_profile.role = 'moderator'
moderator_profile.bio = 'I moderate the community'
moderator_profile.is_email_verified = True
moderator_profile.save()

# Create regular user
regular_user = User.objects.create_user(
    username='user',
    email='user@example.com',
    password='user123',
    first_name='John',
    last_name='Doe'
)
user_profile = regular_user.profile
user_profile.role = 'user'
user_profile.bio = 'Just a regular user'
user_profile.is_email_verified = False
user_profile.save()

print("Creating posts...")

# Create posts from admin
post1 = Post.objects.create(
    title='Welcome to Our GraphQL Community',
    content='This is a welcome post for our new GraphQL community. Feel free to share your questions and experiences!',
    author=admin_user,
    status='published',
    can_comment=True
)

# Create posts from moderator
post2 = Post.objects.create(
    title='GraphQL vs REST API - A Comparison',
    content='Today we discuss the differences between GraphQL and traditional REST APIs. GraphQL provides a more flexible approach to data fetching...',
    author=moderator_user,
    status='published',
    can_comment=True
)

# Create draft post
post3 = Post.objects.create(
    title='Advanced Authentication Patterns',
    content='In this post, we will explore advanced authentication patterns including OAuth2 and JWT tokens...',
    author=moderator_user,
    status='draft',
    can_comment=False
)

# Create posts from regular user
post4 = Post.objects.create(
    title='My First GraphQL Project',
    content='I just built my first GraphQL API using Django and Graphene. It was really interesting to learn about resolvers and input types!',
    author=regular_user,
    status='published',
    can_comment=True
)

post5 = Post.objects.create(
    title='Best Practices for GraphQL Schema Design',
    content='Here are some best practices I learned while designing GraphQL schemas: naming conventions, avoiding deep nesting, using proper types...',
    author=regular_user,
    status='published',
    can_comment=True
)

print("Creating comments...")

# Comments on admin's post
comment1 = Comment.objects.create(
    text='Thanks for creating this community! Looking forward to learning GraphQL.',
    post=post1,
    author=regular_user,
    is_approved=True
)

comment2 = Comment.objects.create(
    text='Great initiative. Hope we can all learn together.',
    post=post1,
    author=moderator_user,
    is_approved=True
)

# Comments on moderator's post
comment3 = Comment.objects.create(
    text='Excellent comparison! GraphQL is definitely more flexible.',
    post=post2,
    author=regular_user,
    is_approved=True
)

comment4 = Comment.objects.create(
    text='This is spam and should be deleted',
    post=post2,
    author=admin_user,
    is_approved=False
)

# Comments on user's posts
comment5 = Comment.objects.create(
    text='Congratulations on your first project!',
    post=post4,
    author=admin_user,
    is_approved=True
)

comment6 = Comment.objects.create(
    text='Can you share the source code?',
    post=post4,
    author=moderator_user,
    is_approved=True
)

comment7 = Comment.objects.create(
    text='Great best practices list!',
    post=post5,
    author=moderator_user,
    is_approved=True
)

comment8 = Comment.objects.create(
    text='What do you think about mutations?',
    post=post5,
    author=admin_user,
    is_approved=True
)

print("Creating activity logs...")

# Log user activities
ActivityLog.objects.create(
    user=admin_user,
    action='login',
    details='Admin login'
)

ActivityLog.objects.create(
    user=admin_user,
    action='create_post',
    details='Created post: Welcome to Our GraphQL Community'
)

ActivityLog.objects.create(
    user=moderator_user,
    action='login',
    details='Moderator login'
)

ActivityLog.objects.create(
    user=moderator_user,
    action='create_post',
    details='Created post: GraphQL vs REST API - A Comparison'
)

ActivityLog.objects.create(
    user=moderator_user,
    action='create_post',
    details='Created post: Advanced Authentication Patterns'
)

ActivityLog.objects.create(
    user=regular_user,
    action='login',
    details='User login'
)

ActivityLog.objects.create(
    user=regular_user,
    action='create_post',
    details='Created post: My First GraphQL Project'
)

ActivityLog.objects.create(
    user=regular_user,
    action='create_post',
    details='Created post: Best Practices for GraphQL Schema Design'
)

ActivityLog.objects.create(
    user=regular_user,
    action='update_profile',
    details='Updated profile information'
)

print("✅ Sample data created successfully!")
print(f"Created {User.objects.count()} users (admin, moderator, user)")
print(f"Created {Post.objects.count()} posts with various statuses")
print(f"Created {Comment.objects.count()} comments (some pending)")
print(f"Created {ActivityLog.objects.count()} activity logs")

print("\nDefault login credentials:")
print("  Admin:      username='admin', password='admin123'")
print("  Moderator:  username='moderator', password='mod123'")
print("  User:       username='user', password='user123'")
