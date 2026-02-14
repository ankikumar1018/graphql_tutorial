"""
Pytest configuration and fixtures for App 2: Mutations & Relationships
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
