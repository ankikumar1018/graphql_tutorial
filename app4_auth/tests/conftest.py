"""
Pytest configuration and fixtures for App 4: Authentication & Authorization
"""
import pytest
import os
import django

# Setup Django settings before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Ensure database is setup for tests"""
    pass


@pytest.fixture(scope='function')
def django_db_reset(django_db_setup, django_db_blocker):
    """Reset database for each test function"""
    with django_db_blocker.unblock():
        from auth_app.models import ActivityLog, Comment, Post, UserProfile
        from django.contrib.auth.models import User
        
        ActivityLog.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
