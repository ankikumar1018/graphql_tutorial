# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(unique=True, db_index=True)),
                ('description', models.TextField(blank=True, default='')),
                ('website', models.URLField(blank=True, null=True)),
                ('employee_count', models.IntegerField(default=0, db_index=True)),
                ('is_active', models.BooleanField(default=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'perf_organization',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('department', models.CharField(db_index=True, max_length=100)),
                ('salary', models.DecimalField(db_index=True, decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('hire_date', models.DateField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='perf_app.organization')),
            ],
            options={
                'db_table': 'perf_employee',
                'ordering': ['-hire_date'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(db_index=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('planning', 'Planning'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('on_hold', 'On Hold')], db_index=True, default='planning', max_length=20)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=12)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('completion_percentage', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='perf_app.organization')),
                ('team_members', models.ManyToManyField(related_name='projects', to='perf_app.employee')),
            ],
            options={
                'db_table': 'perf_project',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_type', models.CharField(choices=[('page_load', 'Page Load Time'), ('api_response', 'API Response Time'), ('database', 'Database Query Time'), ('cache_hit', 'Cache Hit Rate')], db_index=True, max_length=50)),
                ('value', models.FloatField()),
                ('endpoint', models.CharField(db_index=True, max_length=255)),
                ('status_code', models.IntegerField(db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'perf_performance',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(db_index=True, max_length=255)),
                ('test_file', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('passed', 'Passed'), ('failed', 'Failed'), ('skipped', 'Skipped')], db_index=True, max_length=20)),
                ('execution_time', models.FloatField()),
                ('error_message', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'perf_testresult',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='organization',
            index=models.Index(fields=['is_active', 'created_at'], name='perf_organi_is_acti_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['organization', 'is_active'], name='perf_employ_organi_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['department', 'salary'], name='perf_employ_departm_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['organization', 'status'], name='perf_projec_organi_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['status', '-created_at'], name='perf_projec_status_idx'),
        ),
        migrations.AddIndex(
            model_name='performance',
            index=models.Index(fields=['metric_type', 'timestamp'], name='perf_perform_metric_idx'),
        ),
        migrations.AddIndex(
            model_name='performance',
            index=models.Index(fields=['endpoint', '-timestamp'], name='perf_perform_endpoi_idx'),
        ),
        migrations.AddIndex(
            model_name='testresult',
            index=models.Index(fields=['status', 'created_at'], name='perf_testr_status_idx'),
        ),
    ]
