"""
Sample data script for App 5 - Performance, Testing & Production
Demonstrates:
- N+1 query problem (Organization → many Employees)
- M2M relationships (Project → many Team Members)
- Time series data (Performance metrics)
- Test result tracking
"""

import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from perf_app.models import Organization, Employee, Project, Performance, TestResult


def clear_existing_data():
    """Clear existing data"""
    print("Clearing existing data...")
    Performance.objects.all().delete()
    TestResult.objects.all().delete()
    Project.objects.all().delete()
    Employee.objects.all().delete()
    Organization.objects.all().delete()
    print("✓ Data cleared")


def create_organizations():
    """Create sample organizations"""
    print("\nCreating organizations...")
    
    orgs = [
        {
            'name': 'TechCorp International',
            'slug': 'techcorp-intl',
            'description': 'Leading cloud infrastructure and SaaS provider',
            'website': 'https://techcorp.example.com',
            'is_active': True,
            'employee_count': 250
        },
        {
            'name': 'DataFlow Analytics',
            'slug': 'dataflow-analytics',
            'description': 'Big data and analytics solutions',
            'website': 'https://dataflow.example.com',
            'is_active': True,
            'employee_count': 120
        },
        {
            'name': 'SecureNet Security',
            'slug': 'securenet-security',
            'description': 'Cybersecurity and network protection',
            'website': 'https://securenet.example.com',
            'is_active': True,
            'employee_count': 85
        },
        {
            'name': 'CloudPlatform Inc',
            'slug': 'cloudplatform-inc',
            'description': 'Multi-cloud platform management',
            'website': 'https://cloudplatform.example.com',
            'is_active': True,
            'employee_count': 180
        },
        {
            'name': 'DevTools Systems',
            'slug': 'devtools-systems',
            'description': 'Developer tools and IDEs',
            'website': 'https://devtools.example.com',
            'is_active': False,
            'employee_count': 45
        }
    ]
    
    created_orgs = []
    for org_data in orgs:
        org = Organization.objects.create(**org_data)
        created_orgs.append(org)
        print(f"  ✓ Created: {org.name}")
    
    return created_orgs


def create_employees(organizations):
    """Create sample employees (demonstrates N+1 problem)"""
    print("\nCreating employees...")
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'Product', 'Support']
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Iris', 'Jack',
                   'Karen', 'Leo', 'Maya', 'Nathan', 'Olivia', 'Peter', 'Quinn', 'Rachel', 'Sam', 'Tina']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
                  'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
                  'Moore', 'Jackson', 'Martin']
    
    employees = []
    employee_id = 1
    
    # Distribution: 50, 40, 30, 35, 25 employees
    emp_counts = [50, 40, 30, 35, 25]
    
    for org_idx, (org, count) in enumerate(zip(organizations, emp_counts)):
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            department = random.choice(departments)
            salary = random.randint(40000, 150000)
            
            # Vary hire date for last few years
            days_ago = random.randint(0, 365 * 3)
            hire_date = datetime.now() - timedelta(days=days_ago)
            
            emp = Employee.objects.create(
                name=f"{first_name} {last_name}",
                email=f"emp{employee_id}@{org.slug}.com",
                department=department,
                salary=salary,
                organization=org,
                is_active=random.random() > 0.1,  # 90% active
                hire_date=hire_date.date()
            )
            employees.append(emp)
            employee_id += 1
    
    print(f"  ✓ Created {len(employees)} employees across {len(organizations)} organizations")
    return employees


def create_projects(organizations, employees):
    """Create sample projects with team members (M2M relationships)"""
    print("\nCreating projects...")
    
    project_names = [
        'Cloud Migration Initiative',
        'AI/ML Pipeline Development',
        'Mobile App Redesign',
        'Database Optimization',
        'Security Audit & Hardening',
        'API v2 Redesign',
        'Performance Dashboard',
        'Customer Portal Rebuild',
        'Data Integration Platform',
        'Real-time Analytics Engine'
    ]
    
    statuses = ['planning', 'in_progress', 'completed', 'on_hold']
    
    projects = []
    
    for org in organizations:
        if not org.is_active:
            continue
        
        org_employees = [e for e in employees if e.organization_id == org.id]
        if not org_employees:
            continue
        
        # 3-5 projects per active organization
        num_projects = random.randint(3, 5)
        
        for i in range(num_projects):
            project_name = random.choice(project_names)
            budget = random.randint(50000, 500000)
            completion = random.randint(0, 100)
            
            start_date = datetime.now() - timedelta(days=random.randint(30, 180))
            end_date = start_date + timedelta(days=random.randint(30, 120))
            
            project = Project.objects.create(
                name=f"{project_name} - {org.slug}",
                slug=f"{project_name.lower().replace(' ', '-')}-{org.slug}",
                description=f"Strategic project for {org.name}",
                status=random.choice(statuses),
                organization=org,
                budget=budget,
                start_date=start_date.date(),
                end_date=end_date.date(),
                completion_percentage=completion
            )
            
            # Add team members (3-8 employees)
            team_size = random.randint(3, min(8, len(org_employees)))
            team = random.sample(org_employees, team_size)
            project.team_members.set(team)
            
            projects.append(project)
            print(f"  ✓ Created project: {project.name} ({team_size} members)")
    
    return projects


def create_performance_metrics():
    """Create time series performance metrics"""
    print("\nCreating performance metrics...")
    
    metric_types = ['page_load', 'api_response', 'database', 'cache_hit']
    endpoints = [
        '/graphql/',
        '/api/employees',
        '/api/organizations',
        '/api/projects',
        '/api/metrics',
        '/health'
    ]
    
    metrics = []
    
    # Generate metrics for last 7 days
    now = datetime.now()
    
    for metric_type in metric_types:
        for _ in range(50):  # 50 data points per metric type
            timestamp = now - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Realistic values for different metric types
            if metric_type == 'page_load':
                value = random.uniform(100, 3000)  # milliseconds
            elif metric_type == 'api_response':
                value = random.uniform(50, 2000)  # milliseconds
            elif metric_type == 'database':
                value = random.uniform(10, 500)  # milliseconds
            else:  # cache_hit
                value = random.uniform(0, 100)  # percentage
            
            status_code = random.choice([200, 200, 200, 201, 400, 500])  # Most are 200
            
            metric = Performance.objects.create(
                metric_type=metric_type,
                value=value,
                endpoint=random.choice(endpoints),
                status_code=status_code,
                timestamp=timestamp
            )
            metrics.append(metric)
    
    print(f"  ✓ Created {len(metrics)} performance metrics (7 days)")
    return metrics


def create_test_results():
    """Create test result samples"""
    print("\nCreating test results...")
    
    test_files = [
        'test_models.py',
        'test_queries.py',
        'test_performance.py',
        'test_integration.py',
        'test_caching.py'
    ]
    
    test_names = [
        'test_organization_creation',
        'test_employee_fetch',
        'test_project_team_assignment',
        'test_performance_metrics',
        'test_cache_invalidation',
        'test_n_plus_one_prevention',
        'test_aggregations',
        'test_query_optimization'
    ]
    
    statuses = ['passed', 'passed', 'passed', 'failed', 'skipped']  # 60% pass, 20% fail, 20% skip
    
    results = []
    now = datetime.now()
    
    test_cases = 40
    
    for i in range(test_cases):
        test_file = random.choice(test_files)
        test_name = random.choice(test_names)
        status = random.choice(statuses)
        execution_time = random.uniform(0.1, 5.0)  # seconds
        
        if status == 'failed':
            error_msg = f"AssertionError: Expected {random.randint(1, 100)} but got {random.randint(1, 100)}"
        elif status == 'skipped':
            error_msg = "Test skipped: Deprecated functionality"
        else:
            error_msg = "Test passed successfully"
        
        created_at = now - timedelta(
            hours=random.randint(1, 48)
        )
        
        result = TestResult.objects.create(
            test_name=test_name,
            test_file=test_file,
            status=status,
            execution_time=execution_time,
            error_message=error_msg,
            created_at=created_at
        )
        results.append(result)
    
    print(f"  ✓ Created {len(results)} test results")
    return results


def print_summary(orgs, employees, projects, metrics, tests):
    """Print a summary of created data"""
    print("\n" + "="*50)
    print("SAMPLE DATA SUMMARY")
    print("="*50)
    print(f"Organizations: {len(orgs)}")
    print(f"Employees: {len(employees)}")
    print(f"Projects: {len(projects)}")
    print(f"Performance Metrics: {len(metrics)}")
    print(f"Test Results: {len(tests)}")
    print("="*50)
    print("\nN+1 Query Demonstration Setup:")
    print(f"  - {len(orgs)} organizations with {len(employees)} employees total")
    for org in orgs:
        emp_count = org.employees.count()
        print(f"    • {org.name}: {emp_count} employees")
    print("\nM2M Optimization Setup:")
    print(f"  - {len(projects)} projects with team assignments")
    print(f"  - Average team size: {sum(p.team_members.count() for p in projects) / len(projects):.1f} people")
    print("\nTime Series Data:")
    print(f"  - Performance metrics from last 7 days")
    print("\nTest Coverage:")
    passed = len([t for t in tests if t.status == 'passed'])
    failed = len([t for t in tests if t.status == 'failed'])
    print(f"  - Pass rate: {passed}/{len(tests)} ({100*passed/len(tests):.1f}%)")
    print("="*50 + "\n")


if __name__ == '__main__':
    print("🚀 Creating sample data for App 5...\n")
    
    clear_existing_data()
    
    orgs = create_organizations()
    employees = create_employees(orgs)
    projects = create_projects(orgs, employees)
    metrics = create_performance_metrics()
    tests = create_test_results()
    
    print_summary(orgs, employees, projects, metrics, tests)
    
    print("✅ Sample data creation completed!")
    print("\nYou can now:")
    print("  1. Run: python manage.py runserver")
    print("  2. Visit: http://localhost:8000/graphql/")
    print("  3. Import Postman collection: postman/GraphQL-App5-Collection.json")
    print("  4. Test N+1 prevention with DataLoader")
    print("  5. Monitor performance metrics")
