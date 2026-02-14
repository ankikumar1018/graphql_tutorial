from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


class Organization(models.Model):
    """Company/Organization model"""
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True, default='')
    website = models.URLField(blank=True, null=True)
    employee_count = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'perf_organization'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_employee_count_cached(self):
        """Get employee count from cache"""
        cache_key = f'org_employees_{self.id}'
        count = cache.get(cache_key)
        if count is None:
            count = self.employees.filter(is_active=True).count()
            cache.set(cache_key, count, 3600)  # Cache for 1 hour
        return count


class Employee(models.Model):
    """Employee model with many-to-one relationship"""
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    department = models.CharField(max_length=100, db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees', db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    hire_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'perf_employee'
        ordering = ['-hire_date']
        indexes = [
            models.Index(fields=['organization', 'is_active']),
            models.Index(fields=['department', 'salary']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class Project(models.Model):
    """Project model with many-to-many relationship"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects', db_index=True)
    team_members = models.ManyToManyField(Employee, related_name='projects')
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    completion_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'perf_project'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return self.name


class Performance(models.Model):
    """Performance metrics - demonstrates aggregation queries"""
    METRIC_TYPES = [
        ('page_load', 'Page Load Time'),
        ('api_response', 'API Response Time'),
        ('database', 'Database Query Time'),
        ('cache_hit', 'Cache Hit Rate'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES, db_index=True)
    value = models.FloatField()  # milliseconds or percentage
    endpoint = models.CharField(max_length=255, db_index=True)
    status_code = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'perf_performance'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['endpoint', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.value}ms"


class TestResult(models.Model):
    """Test results for testing demonstration"""
    TEST_STATUS = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ]
    
    test_name = models.CharField(max_length=255, db_index=True)
    test_file = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=TEST_STATUS, db_index=True)
    execution_time = models.FloatField()  # seconds
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'perf_testresult'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.test_name} - {self.status}"
