# Quick Start Guide - App 5: Performance & Production

Get up and running in 5 minutes to understand query optimization, caching, and testing patterns.

## 5-Minute Setup

```bash
# 1. Create virtual environment (1 minute)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies (2 minutes)
pip install -r requirements.txt

# 3. Setup database (1 minute)
python manage.py migrate

# 4. Load sample data (1 minute)
python add_sample_data.py

# 5. Start server
python manage.py runserver
```

**Access GraphQL Playground:**
http://localhost:8000/graphql/

## What's in the Sample Data?

```
✓ 5 Organizations
  • TechCorp International (50 employees)
  • DataFlow Analytics (40 employees)
  • SecureNet Security (30 employees)
  • CloudPlatform Inc (35 employees)
  • DevTools Systems (25 employees)

✓ 180 Employees across organizations
  • Demonstrates N+1 query problem and optimization

✓ 18 Projects with team assignments
  • Shows M2M relationship optimization

✓ 200 Performance metrics
  • 7 days of API response times, page loads, DB times

✓ 40 Test results
  • Passed, failed, and skipped tests
```

## 10 Essential Queries

### 1️⃣ Get All Organizations

Shows basic query with caching in background:

```graphql
query {
  allOrganizations {
    id
    name
    slug
    website
    isActive
    createdAt
  }
}
```

**What happens:**
- First call: Database query, result cached for 1 hour
- Subsequent calls: Served from cache (instant)
- Notice: `resolve_all_organizations` uses `cache.get()` and `cache.set()`

---

### 2️⃣ Get Organization with Cached Count

Demonstrates the cached field pattern:

```graphql
query {
  allOrganizations {
    id
    name
    employeeCountCached
    activeEmployeesCount
    projectCount
  }
}
```

**Performance insight:**
- `employeeCountCached`: Uses cache for expensive count
- `activeEmployeesCount`: Filtered count from database
- `projectCount`: Simple M2M count

---

### 3️⃣ Get Employees - N+1 Prevention Example

This is the KEY optimization demonstration:

```graphql
query {
  allEmployees {
    id
    name
    email
    department
    salary
    organization {
      id
      name
    }
    isActive
  }
}
```

**How it works (optimized):**
```python
def resolve_all_employees(self, info):
    # select_related JOINS the organization table
    return Employee.objects.select_related('organization')

# Generates SQL like:
# SELECT employee.*, organization.* FROM employee
# INNER JOIN organization ON ...
# Result: 1 query instead of 1 + N queries
```

**Without optimization (BAD):**
```
Query 1: SELECT * FROM employee (180 rows)
Query 2-181: SELECT * FROM organization WHERE id = X
Total: 181 queries! ❌
```

**With optimization (GOOD):**
```
Query 1: SELECT employee.*, organization.* FROM employee
         INNER JOIN organization ON employee.organization_id = organization.id
Total: 2 queries! ✅
```

**Try it yourself:**
1. Copy the query above
2. Paste in GraphQL Playground
3. Notice in server logs: Only 2 database hits!

---

### 4️⃣ Get Employees by Organization

Filter employees in a specific org:

```graphql
query {
  employeesByOrganization(organizationId: 1) {
    id
    name
    email
    department
    salary
    organizationName
    hireDate
  }
}
```

**Database optimization used:**
- Index on `(organization, is_active)` for fast filtering
- `select_related('organization')` prevents N+1

---

### 5️⃣ Get Project with Team Members (M2M)

Shows M2M optimization with prefetch_related:

```graphql
query {
  project(id: 1) {
    id
    name
    description
    status
    organizationName
    budget
    teamSize
    completionPercentage
    teamMembers {
      id
      name
      email
      department
      salary
    }
  }
}
```

**How it works:**
```python
def resolve_project(self, info, id):
    return Project.objects.prefetch_related('team_members').get(id=id)

# Generates 2 queries:
# Query 1: SELECT * FROM project WHERE id = 1
# Query 2: SELECT * FROM employee 
#          WHERE id IN (SELECT employee_id FROM project_team_members 
#                       WHERE project_id = 1)
# Total: 2 queries (Python matches in memory)
```

**Benefits:**
- Loads all team members in single batch query
- Avoids N queries for M2M

---

### 6️⃣ Get Department Statistics

Aggregation example (COUNT, AVG at database level):

```graphql
query {
  employeeStatsByDepartment {
    department
    count
    averageSalary
  }
}
```

**How it works:**
```python
# Database-level aggregation
dept_stats = Employee.objects.values('department').annotate(
    count=Count('id'),
    avg_salary=Avg('salary')
).order_by('-count')

# Single query with GROUP BY and aggregation functions
# SELECT 
#   department, 
#   COUNT(*) as count,
#   AVG(salary) as avg_salary
# FROM employee
# GROUP BY department
```

**Why it matters:**
- Single database query with aggregation
- NOT loading 180 employees and counting in Python
- 100x faster for large datasets

---

### 7️⃣ Get Performance Metrics Summary

Aggregation for monitoring:

```graphql
query {
  performanceSummary(metricType: "api_response") {
    metricType
    averageValue
    count
    maxValue
    minValue
  }
}
```

**Use cases:**
- API response time monitoring
- Performance SLA tracking (95th percentile)
- Trend analysis over time

---

### 8️⃣ Get Slowest Endpoints

Performance debugging query:

```graphql
query {
  slowestEndpoints(limit: 10) {
    endpoint
    value
    statusCode
    timestamp
  }
}
```

**Application:** Find bottlenecks in production

---

### 9️⃣ Get Test Summary

Test tracking and QA metrics:

```graphql
query {
  testSummary {
    totalTests
    passed
    failed
    skipped
    passRate
    totalExecutionTime
  }
}
```

**Answers:**
- What's our test pass rate?
- How long do tests take?
- How many are skipped?

---

### 🔟 Get Failed Tests

Debugging test failures:

```graphql
query {
  failedTests {
    testName
    testFile
    status
    executionTime
    errorMessage
    createdAt
  }
}
```

**Use case:** CI/CD pipeline monitoring

## Understanding Query Optimization

### The Problem: N+1 Queries

```python
# ❌ SLOW: 51 queries for 50 organizations
organizations = Organization.objects.all()  # Query 1
for org in organizations:  # Queries 2-51
    employees = org.employees.all()  # N+1!
```

### The Solution: select_related()

```python
# ✅ FAST: 2 queries total
organizations = Organization.objects.select_related('employees')
for org in organizations:
    employees = org.employees.all()  # Instant, already loaded
```

### When to Use What

| Relationship | Method | Query Count |
|-------------|--------|------------|
| ForeignKey | `select_related()` | Joins tables (1-2 queries) |
| ManyToMany | `prefetch_related()` | Batch load (2 queries) |
| Reverse FK | `prefetch_related()` | Batch load (2 queries) |

## Caching Patterns

### Simple Cache Example

```graphql
query {
  allOrganizations {
    id
    name
  }
}
```

**What happens:**
1. First call → Database query, cache for 1 hour
2. Subsequent calls → Instant from cache
3. Cache expires → Fresh query runs

**Code:**
```python
def resolve_all_organizations(self, info):
    cache_key = 'all_orgs'
    orgs = cache.get(cache_key)
    if orgs is None:
        orgs = list(Organization.objects.filter(is_active=True))
        cache.set(cache_key, orgs, 3600)  # 1 hour TTL
    return orgs
```

### Per-Entity Caching

```python
# Cache employee count per organization
def get_employee_count_cached(self):
    cache_key = f'org_employees_{self.id}'
    count = cache.get(cache_key)
    if count is None:
        count = self.employees.filter(is_active=True).count()
        cache.set(cache_key, count, 3600)
    return count
```

## Database Indexing

All models include strategic indexes:

```python
class Meta:
    indexes = [
        # Foreign key joins
        models.Index(fields=['organization', 'is_active']),
        # Common filter combinations  
        models.Index(fields=['department', 'salary']),
        # Time series queries
        models.Index(fields=['metric_type', 'timestamp']),
        # "Latest N" queries
        models.Index(fields=['status', '-created_at']),
    ]
```

**Check indexes in PostgreSQL:**
```sql
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'perf_app_employee';
```

## Testing Queries

### Test All Optimizations

```bash
# In GraphQL Playground, run in sequence:

# 1. Basic query
query {
  allOrganizations { name }
}

# 2. With relationships
query {
  allEmployees {
    name
    organization { name }  # ← select_related prevents N+1
  }
}

# 3. M2M relationships
query {
  allProjects {
    name
    teamMembers { name }  # ← prefetch_related optimizes
  }
}

# 4. Aggregations
query {
  employeeStatsByDepartment {
    department
    count
    averageSalary  # ← Database level aggregation
  }
}

# 5. Performance monitoring
query {
  performanceSummary(metricType: "api_response") {
    averageValue
    count
  }
}

# 6. Test results
query {
  testSummary {
    totalTests
    passRate
  }
}
```

## Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure Redis for caching
- [ ] Enable database indexes
- [ ] Setup error tracking (Sentry)
- [ ] Configure logging
- [ ] Enable rate limiting
- [ ] Setup monitoring (Prometheus)
- [ ] Configure SSL/HTTPS
- [ ] Test query performance under load

## Monitoring Tools

### View Database Queries (Development)

```bash
# In Django shell
python manage.py shell
from django.db import connection
from django.test.utils import override_settings

# Enable query tracing
@override_settings(DEBUG=True)
def test_queries():
    from perf_app.models import Employee
    employees = Employee.objects.select_related('organization').all()
    print(len(connection.queries))  # Should be 2, not 182!
```

### Performance Testing

```bash
# Load test with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/graphql/

# With query logging enabled
# Check Django logs for query count and execution time
```

## Common Performance Issues

### Issue: N+1 Queries

```python
# ❌ Bad
orgs = Organization.objects.all()
for org in orgs:
    print(org.employees.count())  # 50 additional queries!

# ✅ Good
orgs = Organization.objects.prefetch_related('employees')
for org in orgs:
    print(org.employees.count())  # Instant, already loaded
```

### Issue: Loading Too Many Fields

```python
# ❌ Bad: Loads 180 employees into memory
employees = list(Employee.objects.all())

# ✅ Good: Lazy evaluation, loads as needed
employees = Employee.objects.all()  # Not evaluated yet
for emp in employees[:10]:  # Only loads 10
    print(emp.name)
```

### Issue: Cache Not Invalidating

```python
# ❌ Bad: Cache never refreshes
def resolve_employees(self, info):
    return cache.get('employees') or []

# ✅ Good: Set explicit TTL
def resolve_employees(self, info):
    cache_key = 'employees'
    emps = cache.get(cache_key)
    if emps is None:
        emps = list(Employee.objects.all())
        cache.set(cache_key, emps, 3600)  # 1 hour
    return emps
```

## Next Steps

1. ✅ Run sample data: `python add_sample_data.py`
2. ✅ Explore GraphQL Playground: http://localhost:8000/graphql/
3. ✅ Try 10 queries above
4. ✅ Study resolver code in config/schema.py
5. ✅ Read README.md for deep dives
6. 🔜 Deploy to production with checklist
7. 🔜 Monitor performance metrics
8. 🔜 Implement caching strategy

## Quick Tips

**Enable Query Logging:**
```python
# settings.py
LOGGING = {
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # See all queries
        },
    },
}
```

**Use Django Debug Toolbar (dev only):**
```bash
pip install django-debug-toolbar

# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

**Profiling with Django Shell:**
```python
python manage.py shell
import django
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True

from perf_app.models import Employee
reset_queries()
employees = Employee.objects.select_related('organization').all()
list(employees)  # Force evaluation

print(f"Executed {len(connection.queries)} queries")
for q in connection.queries:
    print(f"  {q['time']}ms: {q['sql'][:100]}")
```

---

**Total Setup Time: ~5 minutes**
**Learning Time: ~30 minutes**
**Deployment Time: ~2 hours**

Questions? Check README.md for detailed explanations.
