import graphene
from graphene_django import DjangoObjectType
from graphene.types.schema import Schema
from promise import Promise
from django.db import models
from django.db.models import Avg, Count, Q, Max, Min, Sum
from django.core.cache import cache
from perf_app.models import Organization, Employee, Project, Performance, TestResult


# ==================== DataLoader Pattern (N+1 Prevention) ====================

class DataLoader:
    """Simple DataLoader implementation for batch operations"""
    def __init__(self, batch_fn):
        self.batch_fn = batch_fn
        self.queue = []
        self.cache = {}
    
    def load(self, key):
        """Load a value, batching requests"""
        if key in self.cache:
            return Promise.resolve(self.cache[key])
        
        promise = Promise(lambda resolve, reject: None)
        self.queue.append((key, promise))
        
        return promise
    
    def dispatch(self):
        """Execute all pending batches"""
        if not self.queue:
            return
        
        keys = [key for key, _ in self.queue]
        results = self.batch_fn(keys)
        
        for (key, promise), result in zip(self.queue, results):
            self.cache[key] = result
            promise.resolve(result)
        
        self.queue = []


# ==================== GraphQL Types ====================

class OrganizationType(DjangoObjectType):
    """Organization type with optimized employee count"""
    employee_count_cached = graphene.Int()
    total_budget = graphene.Float()
    active_employees_count = graphene.Int()
    project_count = graphene.Int()
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'description', 'website', 'is_active', 'created_at']
    
    def resolve_employee_count_cached(self, info):
        """Get employee count from cache"""
        return self.get_employee_count_cached()
    
    def resolve_total_budget(self, info):
        """Calculate total project budget"""
        cache_key = f'org_budget_{self.id}'
        budget = cache.get(cache_key)
        if budget is None:
            budget = sum(float(p.budget) for p in self.projects.all())
            cache.set(cache_key, budget, 3600)
        return budget
    
    def resolve_active_employees_count(self, info):
        """Count active employees"""
        return self.employees.filter(is_active=True).count()
    
    def resolve_project_count(self, info):
        """Count all projects"""
        return self.projects.count()


class EmployeeType(DjangoObjectType):
    """Employee type"""
    organization_name = graphene.String()
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'salary', 'organization', 'is_active', 'hire_date']
    
    def resolve_organization_name(self, info):
        """Get organization name"""
        return self.organization.name


class ProjectType(DjangoObjectType):
    """Project type"""
    organization_name = graphene.String()
    team_size = graphene.Int()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'description', 'status', 'organization', 'team_members', 'budget', 'start_date', 'end_date', 'completion_percentage']
    
    def resolve_organization_name(self, info):
        """Get organization name"""
        return self.organization.name
    
    def resolve_team_size(self, info):
        """Get team member count"""
        return self.team_members.count()


class PerformanceType(DjangoObjectType):
    """Performance metrics type"""
    class Meta:
        model = Performance
        fields = ['id', 'metric_type', 'value', 'endpoint', 'status_code', 'timestamp']


class TestResultType(DjangoObjectType):
    """Test result type"""
    class Meta:
        model = TestResult
        fields = ['id', 'test_name', 'test_file', 'status', 'execution_time', 'error_message', 'created_at']


class PerformanceMetricsType(graphene.ObjectType):
    """Aggregated performance metrics"""
    metric_type = graphene.String()
    average_value = graphene.Float()
    count = graphene.Int()
    max_value = graphene.Float()
    min_value = graphene.Float()


class TestSummaryType(graphene.ObjectType):
    """Test execution summary"""
    total_tests = graphene.Int()
    passed = graphene.Int()
    failed = graphene.Int()
    skipped = graphene.Int()
    pass_rate = graphene.Float()
    total_execution_time = graphene.Float()


class EmployeeStatsType(graphene.ObjectType):
    """Employee statistics for a department"""
    department = graphene.String()
    count = graphene.Int()
    average_salary = graphene.Float()


# ==================== Queries ====================

class Query(graphene.ObjectType):
    """All queries with optimization examples"""
    
    # Organization queries
    organization = graphene.Field(OrganizationType, id=graphene.Int(required=True))
    all_organizations = graphene.List(OrganizationType)
    organizations_by_status = graphene.List(OrganizationType, is_active=graphene.Boolean())
    
    # Employee queries
    employee = graphene.Field(EmployeeType, id=graphene.Int(required=True))
    all_employees = graphene.List(EmployeeType)
    employees_by_organization = graphene.List(EmployeeType, organization_id=graphene.Int(required=True))
    employees_by_department = graphene.List(EmployeeType, department=graphene.String(required=True))
    expensive_employees = graphene.List(EmployeeType, min_salary=graphene.Float(required=True))
    
    # Project queries
    project = graphene.Field(ProjectType, id=graphene.Int(required=True))
    all_projects = graphene.List(ProjectType)
    projects_by_status = graphene.List(ProjectType, status=graphene.String(required=True))
    projects_by_organization = graphene.List(ProjectType, organization_id=graphene.Int(required=True))
    
    # Performance monitoring
    performance_metrics = graphene.List(PerformanceType, metric_type=graphene.String())
    performance_summary = graphene.Field(PerformanceMetricsType, metric_type=graphene.String(required=True))
    slowest_endpoints = graphene.List(PerformanceType, limit=graphene.Int())
    
    # Testing
    test_results = graphene.List(TestResultType, status=graphene.String())
    test_summary = graphene.Field(TestSummaryType)
    failed_tests = graphene.List(TestResultType)
    
    # Statistics & Aggregations
    employee_stats_by_department = graphene.List(EmployeeStatsType)
    
    # ==================== Resolvers ====================
    
    def resolve_organization(self, info, id):
        """Get organization by ID - with select_related"""
        try:
            return Organization.objects.get(id=id)
        except Organization.DoesNotExist:
            return None
    
    def resolve_all_organizations(self, info):
        """Get all organizations - with caching"""
        cache_key = 'all_orgs'
        orgs = cache.get(cache_key)
        if orgs is None:
            orgs = list(Organization.objects.filter(is_active=True))
            cache.set(cache_key, orgs, 3600)
        return orgs
    
    def resolve_organizations_by_status(self, info, is_active):
        """Filter organizations by active status"""
        return Organization.objects.filter(is_active=is_active)
    
    def resolve_employee(self, info, id):
        """Get employee by ID - with select_related"""
        try:
            return Employee.objects.select_related('organization').get(id=id)
        except Employee.DoesNotExist:
            return None
    
    def resolve_all_employees(self, info):
        """Get all employees - with prefetch_related for optimization"""
        return Employee.objects.select_related('organization').filter(is_active=True)
    
    def resolve_employees_by_organization(self, info, organization_id):
        """Get employees in organization"""
        return Employee.objects.filter(
            organization_id=organization_id,
            is_active=True
        ).select_related('organization')
    
    def resolve_employees_by_department(self, info, department):
        """Get employees in department"""
        return Employee.objects.filter(
            department=department,
            is_active=True
        ).select_related('organization')
    
    def resolve_expensive_employees(self, info, min_salary):
        """Get employees earning above threshold"""
        return Employee.objects.filter(
            salary__gte=min_salary,
            is_active=True
        ).select_related('organization').order_by('-salary')[:20]
    
    def resolve_project(self, info, id):
        """Get project by ID - with prefetch_related for M2M"""
        try:
            return Project.objects.prefetch_related('team_members').select_related('organization').get(id=id)
        except Project.DoesNotExist:
            return None
    
    def resolve_all_projects(self, info):
        """Get all projects - with optimization"""
        return Project.objects.prefetch_related('team_members').select_related('organization')
    
    def resolve_projects_by_status(self, info, status):
        """Get projects by status"""
        return Project.objects.filter(status=status).prefetch_related('team_members').select_related('organization')
    
    def resolve_projects_by_organization(self, info, organization_id):
        """Get projects for organization"""
        return Project.objects.filter(
            organization_id=organization_id
        ).prefetch_related('team_members').select_related('organization')
    
    def resolve_performance_metrics(self, info, metric_type=None):
        """Get performance metrics"""
        queryset = Performance.objects.all()
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)
        return queryset.order_by('-timestamp')[:100]
    
    def resolve_performance_summary(self, info, metric_type):
        """Get aggregated performance metrics"""
        metrics = Performance.objects.filter(metric_type=metric_type).aggregate(
            avg_value=Avg('value'),
            count=Count('id'),
            max_value=Max('value'),
            min_value=Min('value')
        )
        
        return PerformanceMetricsType(
            metric_type=metric_type,
            average_value=metrics['avg_value'],
            count=metrics['count'],
            max_value=metrics['max_value'],
            min_value=metrics['min_value']
        )
    
    def resolve_slowest_endpoints(self, info, limit=None):
        """Get slowest API endpoints"""
        limit = limit or 10
        return Performance.objects.filter(
            metric_type='api_response'
        ).order_by('-value')[:limit]
    
    def resolve_test_results(self, info, status=None):
        """Get test results"""
        queryset = TestResult.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')[:100]
    
    def resolve_test_summary(self, info):
        """Get test execution summary"""
        results = TestResult.objects.aggregate(
            total=Count('id'),
            passed=Count('id', filter=Q(status='passed')),
            failed=Count('id', filter=Q(status='failed')),
            skipped=Count('id', filter=Q(status='skipped')),
            total_time=Sum('execution_time')
        )
        
        total = results['total'] or 1
        pass_rate = (results['passed'] / total) * 100 if total > 0 else 0
        
        return TestSummaryType(
            total_tests=results['total'],
            passed=results['passed'],
            failed=results['failed'],
            skipped=results['skipped'],
            pass_rate=pass_rate,
            total_execution_time=results['total_time'] or 0.0
        )
    
    def resolve_failed_tests(self, info):
        """Get failed tests"""
        return TestResult.objects.filter(status='failed').order_by('-created_at')[:50]
    
    def resolve_employee_stats_by_department(self, info):
        """Statistics by department"""
        from django.db.models import Avg
        stats = Employee.objects.filter(is_active=True).values('department').annotate(
            count=Count('id'),
            avg_salary=Avg('salary')
        ).order_by('-count')
        
        return [
            EmployeeStatsType(
                department=s['department'],
                count=s['count'],
                average_salary=float(s['avg_salary'])
            )
            for s in stats
        ]


schema = graphene.Schema(query=Query)
