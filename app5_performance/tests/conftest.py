"""
Pytest configuration and fixtures for App 5: Performance & Optimization
"""
import pytest
import os
import django
from django.core.cache import cache

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
        from perf_app.models import TestResult, Performance, Project, Employee, Organization
        
        TestResult.objects.all().delete()
        Performance.objects.all().delete()
        Project.objects.all().delete()
        Employee.objects.all().delete()
        Organization.objects.all().delete()


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test"""
    cache.clear()
    yield
    cache.clear()
