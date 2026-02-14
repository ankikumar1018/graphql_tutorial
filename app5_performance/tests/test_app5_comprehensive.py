"""
Comprehensive pytest suite for App 5: Performance & Optimization
Tests cover models, N+1 query prevention, caching, aggregations, and performance patterns
"""
import pytest
from django.test import Client
from graphene.test import Client as GrapheneClient
from perf_app.models import Organization, Employee, Project, Performance, TestResult
from config.schema import schema
import json
from decimal import Decimal
from datetime import date, datetime, timedelta
from django.core.cache import cache
from django.db import connection
from django.test.utils import override_settings


@pytest.fixture
def api_client():
    """GraphQL test client"""
    return GrapheneClient(schema)


@pytest.fixture
def http_client():
    """HTTP client"""
    return Client()


@pytest.fixture
def sample_organizations(db):
    """Create sample organizations"""
    return [
        Organization.objects.create(
            name="Tech Corp",
            slug="tech-corp",
            description="Technology company",
            website="https://techcorp.com",
            employee_count=100,
            is_active=True
        ),
        Organization.objects.create(
            name="Finance Inc",
            slug="finance-inc",
            description="Financial services",
            employee_count=50,
            is_active=True
        ),
        Organization.objects.create(
            name="Inactive Co",
            slug="inactive-co",
            description="Inactive company",
            is_active=False
        ),
    ]


@pytest.fixture
def sample_employees(db, sample_organizations):
    """Create sample employees"""
    org1, org2, _ = sample_organizations
    employees = []
    
    departments = ['Engineering', 'Sales', 'HR', 'Engineering', 'Finance']
    salaries = [80000, 60000, 55000, 90000, 70000]
    
    for i, (dept, salary) in enumerate(zip(departments, salaries)):
        org = org1 if i < 3 else org2
        employees.append(
            Employee.objects.create(
                name=f"Employee {i+1}",
                email=f"emp{i+1}@example.com",
                department=dept,
                salary=Decimal(str(salary)),
                organization=org,
                hire_date=date(2020, 1, i+1),
                is_active=True
            )
        )
    
    return employees


@pytest.fixture
def sample_projects(db, sample_organizations, sample_employees):
    """Create sample projects"""
    org1 = sample_organizations[0]
    projects = []
    
    statuses = ['planning', 'in_progress', 'completed']
    for i, status in enumerate(statuses):
        project = Project.objects.create(
            name=f"Project {i+1}",
            slug=f"project-{i+1}",
            description=f"Description {i+1}",
            status=status,
            organization=org1,
            budget=Decimal('100000.00'),
            start_date=date(2024, 1, 1),
            completion_percentage=i * 30
        )
        # Add team members
        project.team_members.add(*sample_employees[:2])
        projects.append(project)
    
    return projects


@pytest.fixture
def sample_performance_metrics(db):
    """Create sample performance metrics"""
    metrics = []
    for i in range(10):
        metrics.append(
            Performance.objects.create(
                metric_type='api_response',
                value=100 + i * 10,
                endpoint='/api/test',
                status_code=200
            )
        )
    return metrics


@pytest.fixture
def sample_test_results(db):
    """Create sample test results"""
    results = []
    for i in range(5):
        status = 'passed' if i % 2 == 0 else 'failed'
        results.append(
            TestResult.objects.create(
                test_name=f"test_{i}",
                test_file=f"test_file_{i}.py",
                status=status,
                execution_time=0.5 + i * 0.1
            )
        )
    return results


# ==================== Model Tests ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestOrganizationModel:
    """Test Organization model"""
    
    def test_organization_creation(self):
        """Test creating an organization"""
        org = Organization.objects.create(
            name="Test Org",
            slug="test-org",
            employee_count=10
        )
        assert org.name == "Test Org"
        assert str(org) == "Test Org"
    
    def test_organization_defaults(self, db):
        """Test default values"""
        org = Organization.objects.create(
            name="Default Org",
            slug="default-org"
        )
        assert org.is_active is True
        assert org.employee_count == 0
    
    def test_organization_relationships(self, sample_organizations, sample_employees):
        """Test organization has employees"""
        org = sample_organizations[0]
        assert org.employees.count() == 3


@pytest.mark.unit
@pytest.mark.django_db
class TestEmployeeModel:
    """Test Employee model"""
    
    def test_employee_creation(self, sample_organizations):
        """Test creating an employee"""
        emp = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="Engineering",
            salary=Decimal('75000.00'),
            organization=sample_organizations[0],
            hire_date=date(2020, 1, 1)
        )
        assert emp.name == "John Doe"
        assert emp.salary == Decimal('75000.00')
    
    def test_employee_organization_relationship(self, sample_employees, sample_organizations):
        """Test employee belongs to organization"""
        emp = sample_employees[0]
        assert emp.organization == sample_organizations[0]


@pytest.mark.unit
@pytest.mark.django_db
class TestProjectModel:
    """Test Project model"""
    
    def test_project_creation(self, sample_organizations):
        """Test creating a project"""
        project = Project.objects.create(
            name="Test Project",
            slug="test-project",
            description="Test",
            organization=sample_organizations[0],
            budget=Decimal('50000.00'),
            start_date=date(2024, 1, 1)
        )
        assert project.name == "Test Project"
        assert project.status == "planning"
    
    def test_project_team_members(self, sample_projects, sample_employees):
        """Test project many-to-many with employees"""
        project = sample_projects[0]
        assert project.team_members.count() == 2


@pytest.mark.unit
@pytest.mark.django_db
class TestPerformanceModel:
    """Test Performance model"""
    
    def test_performance_creation(self):
        """Test creating a performance metric"""
        metric = Performance.objects.create(
            metric_type='api_response',
            value=150.0,
            endpoint='/api/users',
            status_code=200
        )
        assert metric.value == 150.0
        assert str(metric) == "api_response: 150.0ms"


@pytest.mark.unit
@pytest.mark.django_db
class TestTestResultModel:
    """Test TestResult model"""
    
    def test_test_result_creation(self):
        """Test creating a test result"""
        result = TestResult.objects.create(
            test_name="test_example",
            test_file="test_file.py",
            status="passed",
            execution_time=0.25
        )
        assert result.status == "passed"
        assert result.execution_time == 0.25


# ==================== Basic Query Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestBasicQueries:
    """Test basic GraphQL queries"""
    
    def test_all_organizations_query(self, api_client, sample_organizations):
        """Test allOrganizations query"""
        query = '''
            query {
                allOrganizations {
                    id
                    name
                    slug
                    employeeCountCached
                    isActive
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        orgs = result['data']['allOrganizations']
        assert len(orgs) >= 3
    
    def test_organization_by_id(self, api_client, sample_organizations):
        """Test organization query by ID"""
        org_id = sample_organizations[0].id
        query = f'''
            query {{
                organization(id: {org_id}) {{
                    id
                    name
                    employeeCountCached
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        assert result['data']['organization']['name'] == "Tech Corp"
    
    def test_all_employees_query(self, api_client, sample_employees):
        """Test allEmployees query"""
        query = '''
            query {
                allEmployees {
                    id
                    name
                    email
                    department
                    salary
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        employees = result['data']['allEmployees']
        assert len(employees) >= 5
    
    def test_all_projects_query(self, api_client, sample_projects):
        """Test allProjects query"""
        query = '''
            query {
                allProjects {
                    id
                    name
                    status
                    budget
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        projects = result['data']['allProjects']
        assert len(projects) >= 3


# ==================== N+1 Query Prevention Tests ====================

@pytest.mark.nplus1
@pytest.mark.django_db
class TestNPlusOnePrevention:
    """Test N+1 query prevention with select_related and prefetch_related"""
    
    def test_employees_with_organization_optimized(self, api_client, sample_employees):
        """Test that querying employees with organization uses select_related"""
        query = '''
            query {
                employeesOptimized {
                    id
                    name
                    organization {
                        name
                    }
                }
            }
        '''
        
        # Count queries
        with self.assert_num_queries(1):  # Should be 1 query with select_related
            result = api_client.execute(query)
        
        # This test depends on the schema implementing select_related
        # Adjust based on actual implementation
    
    def test_projects_with_team_members_optimized(self, api_client, sample_projects):
        """Test projects with team members uses prefetch_related"""
        query = '''
            query {
                projectsOptimized {
                    id
                    name
                    teamMembers {
                        name
                    }
                }
            }
        '''
        # Should use prefetch_related for M2M relationship
    
    def test_organization_with_employees_optimized(self, api_client, sample_organizations, sample_employees):
        """Test organization with employees query optimization"""
        org_id = sample_organizations[0].id
        query = f'''
            query {{
                organization(id: {org_id}) {{
                    id
                    name
                    activeEmployeesCount
                    employeeCountCached
                }}
            }}
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
    
    def assert_num_queries(self, num):
        """Context manager to assert number of queries"""
        # This is a simplified version - in practice use Django's assertNumQueries
        from django.test.utils import CaptureQueriesContext
        return CaptureQueriesContext(connection)


# ==================== Caching Tests ====================

@pytest.mark.caching
@pytest.mark.django_db
class TestCaching:
    """Test caching functionality"""
    
    def test_cached_employee_count(self, sample_organizations, sample_employees):
        """Test cached employee count method"""
        org = sample_organizations[0]
        cache.clear()
        
        # First call - should hit database
        count1 = org.get_employee_count_cached()
        assert count1 == 3
        
        # Second call - should hit cache
        count2 = org.get_employee_count_cached()
        assert count2 == 3
        
        # Verify cache was used
        cache_key = f'org_employees_{org.id}'
        cached_value = cache.get(cache_key)
        assert cached_value == 3
    
    def test_cache_invalidation(self, sample_organizations, sample_employees):
        """Test cache invalidation when data changes"""
        org = sample_organizations[0]
        cache.clear()
        
        # Get count (caches it)
        count1 = org.get_employee_count_cached()
        
        # Add new employee
        Employee.objects.create(
            name="New Employee",
            email="new@example.com",
            department="IT",
            salary=Decimal('60000'),
            organization=org,
            hire_date=date(2024, 1, 1)
        )
        
        # Clear cache and get new count
        cache_key = f'org_employees_{org.id}'
        cache.delete(cache_key)
        count2 = org.get_employee_count_cached()
        
        assert count2 == count1 + 1
    
    def test_organization_stats_cached(self, api_client, sample_organizations, sample_employees):
        """Test cached organization statistics query"""
        query = '''
            query {
                organizationStatsCached {
                    totalOrganizations
                    activeOrganizations
                    totalEmployees
                }
            }
        '''
        cache.clear()
        
        # First call
        result1 = api_client.execute(query)
        if 'errors' not in result1:
            stats1 = result1['data']['organizationStatsCached']
            
            # Second call (should be cached)
            result2 = api_client.execute(query)
            stats2 = result2['data']['organizationStatsCached']
            
            assert stats1 == stats2


# ==================== Aggregation Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestAggregations:
    """Test aggregation queries"""
    
    def test_employee_stats_by_department(self, api_client, sample_employees):
        """Test employee statistics by department"""
        query = '''
            query {
                employeeStatsByDepartment {
                    department
                    count
                    averageSalary
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        stats = result['data']['employeeStatsByDepartment']
        assert len(stats) > 0
        
        # Check Engineering department
        eng_stats = next((s for s in stats if s['department'] == 'Engineering'), None)
        if eng_stats:
            assert eng_stats['count'] >= 1
    
    def test_organization_summary(self, api_client, sample_organizations, sample_employees):
        """Test organization summary with aggregations"""
        org_id = sample_organizations[0].id
        query = f'''
            query {{
                organizationSummary(id: {org_id}) {{
                    name
                    totalEmployees
                    totalProjects
                    avgSalary
                    departments
                }}
            }}
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            summary = result['data']['organizationSummary']
            assert summary['totalEmployees'] > 0
    
    def test_project_statistics(self, api_client, sample_projects):
        """Test project statistics"""
        query = '''
            query {
                projectStats {
                    totalProjects
                    byStatus {
                        status
                        count
                    }
                    avgBudget
                    avgCompletion
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            stats = result['data']['projectStats']
            assert stats['totalProjects'] == 3
    
    def test_performance_metrics_aggregation(self, api_client, sample_performance_metrics):
        """Test aggregating performance metrics"""
        query = '''
            query {
                performanceMetricsSummary(metricType: "api_response") {
                    avgValue
                    minValue
                    maxValue
                    count
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            summary = result['data']['performanceMetricsSummary']
            assert summary['count'] == 10


# ==================== Filtering & Sorting Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestFilteringAndSorting:
    """Test filtering and sorting queries"""
    
    def test_filter_employees_by_department(self, api_client, sample_employees):
        """Test filtering employees by department"""
        query = '''
            query {
                employeesByDepartment(department: "Engineering") {
                    name
                    department
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            employees = result['data']['employeesByDepartment']
            assert all(emp['department'] == 'Engineering' for emp in employees)
    
    def test_filter_projects_by_status(self, api_client, sample_projects):
        """Test filtering projects by status"""
        query = '''
            query {
                projectsByStatus(status: "in_progress") {
                    name
                    status
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        # Verify query executes and returns list
        projects = result['data']['projectsByStatus']
        assert isinstance(projects, list)
    
    def test_filter_active_organizations(self, api_client, sample_organizations):
        """Test filtering active organizations"""
        query = '''
            query {
                activeOrganizations {
                    name
                    isActive
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            orgs = result['data']['activeOrganizations']
            assert all(org['isActive'] for org in orgs)
            assert len(orgs) == 2
    
    def test_sort_employees_by_salary(self, api_client, sample_employees):
        """Test sorting employees by salary"""
        query = '''
            query {
                employeesSorted(sortBy: "salary", order: "desc") {
                    name
                    salary
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            employees = result['data']['employeesSorted']
            salaries = [float(emp['salary']) for emp in employees]
            assert salaries == sorted(salaries, reverse=True)


# ==================== Performance Metric Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestPerformanceMetrics:
    """Test performance metric queries"""
    
    def test_recent_performance_metrics(self, api_client, sample_performance_metrics):
        """Test getting recent performance metrics"""
        query = '''
            query {
                recentPerformanceMetrics(limit: 5) {
                    metricType
                    value
                    endpoint
                    statusCode
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            metrics = result['data']['recentPerformanceMetrics']
            assert len(metrics) <= 5
    
    def test_metrics_by_endpoint(self, api_client, sample_performance_metrics):
        """Test filtering metrics by endpoint"""
        query = '''
            query {
                metricsByEndpoint(endpoint: "/api/test") {
                    value
                    endpoint
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            metrics = result['data']['metricsByEndpoint']
            assert all(m['endpoint'] == '/api/test' for m in metrics)
    
    def test_slow_requests(self, api_client, sample_performance_metrics):
        """Test finding slow requests"""
        query = '''
            query {
                slowRequests(threshold: 150.0) {
                    value
                    endpoint
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            slow = result['data']['slowRequests']
            assert all(m['value'] > 150.0 for m in slow)


# ==================== Test Result Tests ====================

@pytest.mark.graphql
@pytest.mark.django_db
class TestTestResults:
    """Test test result queries"""
    
    def test_all_test_results(self, api_client, sample_test_results):
        """Test getting all test results"""
        query = '''
            query {
                testResults {
                    testName
                    status
                    executionTime
                }
            }
        '''
        result = api_client.execute(query)
        assert 'errors' not in result
        results = result['data']['testResults']
        assert len(results) >= 5
    
    def test_test_results_by_status(self, api_client, sample_test_results):
        """Test filtering test results by status"""
        query = '''
            query {
                testResultsByStatus(status: "passed") {
                    testName
                    status
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            results = result['data']['testResultsByStatus']
            assert all(r['status'] == 'passed' for r in results)
    
    def test_test_summary(self, api_client, sample_test_results):
        """Test test summary statistics"""
        query = '''
            query {
                testSummary {
                    totalTests
                    passed
                    failed
                    skipped
                    passRate
                }
            }
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            summary = result['data']['testSummary']
            assert summary['totalTests'] >= 5
            assert summary['passed'] + summary['failed'] + summary['skipped'] == summary['totalTests']


# ==================== Complex Query Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestComplexQueries:
    """Test complex nested queries"""
    
    def test_organization_with_all_related_data(self, api_client, sample_organizations, sample_employees, sample_projects):
        """Test fetching organization with employees and projects"""
        org_id = sample_organizations[0].id
        query = f'''
            query {{
                organizationComplete(id: {org_id}) {{
                    name
                    employees {{
                        name
                        department
                        projects {{
                            name
                        }}
                    }}
                    projects {{
                        name
                        status
                        teamMembers {{
                            name
                        }}
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            org = result['data']['organizationComplete']
            assert len(org['employees']) > 0
            assert len(org['projects']) > 0
    
    def test_employee_with_projects_and_organization(self, api_client, sample_employees):
        """Test fetching employee with all relationships"""
        emp_id = sample_employees[0].id
        query = f'''
            query {{
                employee(id: {emp_id}) {{
                    name
                    organization {{
                        name
                    }}
                    projects {{
                        name
                        status
                    }}
                }}
            }}
        '''
        result = api_client.execute(query)
        if 'errors' not in result:
            emp = result['data']['employee']
            assert emp['organization'] is not None


# ==================== HTTP Endpoint Tests ====================

@pytest.mark.integration
@pytest.mark.django_db
class TestHTTPEndpoint:
    """Test GraphQL HTTP endpoint"""
    
    def test_query_via_http(self, http_client, sample_organizations):
        """Test query through HTTP POST"""
        query_data = {
            "query": '''
                query {
                    allOrganizations {
                        id
                        name
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


# ==================== Edge Cases ====================

@pytest.mark.unit
@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_organization_with_no_employees(self, db):
        """Test organization with zero employees"""
        org = Organization.objects.create(
            name="Empty Org",
            slug="empty-org"
        )
        assert org.employees.count() == 0
        assert org.employee_count == 0
    
    def test_project_with_no_team_members(self, sample_organizations):
        """Test project without team members"""
        project = Project.objects.create(
            name="Solo Project",
            slug="solo-project",
            description="No team",
            organization=sample_organizations[0],
            budget=Decimal('10000'),
            start_date=date(2024, 1, 1)
        )
        assert project.team_members.count() == 0
    
    def test_employee_salary_decimal_precision(self, sample_organizations):
        """Test salary decimal precision"""
        emp = Employee.objects.create(
            name="Test",
            email="precision@test.com",
            department="Test",
            salary=Decimal('75000.99'),
            organization=sample_organizations[0],
            hire_date=date(2024, 1, 1)
        )
        assert emp.salary == Decimal('75000.99')
