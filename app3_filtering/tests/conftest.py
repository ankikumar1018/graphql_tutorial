"""
Pytest configuration and fixtures for App 3: Filtering, Sorting, Pagination
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
        from filtering_app.models import Category, Product, Review
        Review.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
