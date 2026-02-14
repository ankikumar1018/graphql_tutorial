from django.contrib import admin
from perf_app.models import Organization, Employee, Project, Performance, TestResult


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'employee_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'organization', 'salary', 'is_active']
    list_filter = ['department', 'is_active', 'hire_date']
    search_fields = ['name', 'email', 'organization__name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'organization', 'completion_percentage', 'created_at']
    list_filter = ['status', 'organization', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['team_members']


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'endpoint', 'value', 'status_code', 'timestamp']
    list_filter = ['metric_type', 'status_code', 'timestamp']
    search_fields = ['endpoint']
    readonly_fields = ['timestamp']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'status', 'execution_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['test_name', 'test_file']
    readonly_fields = ['created_at']
