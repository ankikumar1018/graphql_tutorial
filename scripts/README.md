# GraphQL Django Test Scripts

This directory contains bash scripts for running tests across all GraphQL Django tutorial apps with automated virtual environment setup and cleanup.

## Scripts Overview

### 🚀 `run_all_tests.sh`
Runs tests for all 5 apps with automatic environment setup and cleanup.

**Automatic Cleanup:**
- Removes `.coverage*` and `coverage.xml` files
- Deletes `__pycache__` and `.pytest_cache` directories
- Cleans up all test artifacts after completion
- Preserves HTML coverage reports for review

**Usage:**
```bash
./scripts/run_all_tests.sh [pytest_options]
```

**Features:**
- Creates isolated virtual environment (`.venv_tests`)
- Installs dependencies from `dev-requirements.txt`
- Runs tests for all 5 apps sequentially
- Generates individual coverage reports per app
- Displays test summary with pass/fail status
- **Automatically cleans up temporary files on exit**

**Examples:**
```bash
# Run all tests with default settings
./scripts/run_all_tests.sh

# Run with quiet output
./scripts/run_all_tests.sh -q

# Run with coverage reports
./scripts/run_all_tests.sh --cov=config --cov=perf_app

# Run with verbose output
./scripts/run_all_tests.sh -v
```

**Exit Codes:**
- `0` - All apps passed
- `1` - One or more apps failed

---

### 🎯 `run_single_app.sh`
Runs tests for a single app with automatic environment setup and cleanup.

**Automatic Cleanup:**
- Removes `.coverage*` and `coverage.xml` files
- Deletes `__pycache__` and `.pytest_cache` directories
- Cleans up all test artifacts after completion
- Preserves HTML coverage reports for review

**Usage:**
```bash
./scripts/run_single_app.sh <app_name> [pytest_options]
```

**Available Apps:**
- `app1_basics` - Basic queries
- `app2_mutations` - Mutations and relationships
- `app3_filtering` - Filtering and pagination
- `app4_auth` - Authentication and authorization
- `app5_performance` - Performance optimization

**Features:**
- Creates/reuses virtual environment
- Installs/updates dependencies as needed
- Runs tests for specified app
- Generates HTML coverage report
- **Automatically cleans up temporary files on exit**

**Examples:**
```bash
# Run app1 tests
./scripts/run_single_app.sh app1_basics

# Run app2 with verbose output
./scripts/run_single_app.sh app2_mutations -v

# Run app4 with coverage
./scripts/run_single_app.sh app4_auth --cov=auth_app

# Run app5 with short traceback
./scripts/run_single_app.sh app5_performance --tb=short
```

---

### 🧹 `cleanup.sh`
Manual cleanup utility for complete environment reset (optional - automatic cleanup happens during test runs).

**Usage:**
```bash
./scripts/cleanup.sh
```

**Removes:**
- Virtual environment (`.venv_tests`)
- Coverage data files (`.coverage*`, `coverage.xml`)
- Pytest cache (`__pycache__`, `.pytest_cache`)
- HTML coverage reports (`htmlcov/` directories)

**When to Use:**
- Manual cleanup between different test environments
- Complete reset when switching Python versions
- CI/CD cleanup steps
- **Note:** Automatic cleanup already runs after each test execution

---

## Automatic Cleanup

Both `run_all_tests.sh` and `run_single_app.sh` automatically clean up test artifacts when complete:

**Removed Automatically:**
- `.coverage` and `.coverage.*` files
- `coverage.xml` reports
- `__pycache__` directories
- `.pytest_cache` directories

**Preserved for Review:**
- HTML coverage reports (`htmlcov/`)
- Virtual environment (`.venv_tests/`)
- Source code and configuration files

This ensures your workspace stays clean without manual intervention.

---

## Dependency Management

### `dev-requirements.txt`
Contains all testing dependencies for the GraphQL Django apps.

**Install manually:**
```bash
pip install -r scripts/dev-requirements.txt
```

**Included packages:**
- Django 4.2.7
- Graphene 3.3 & graphene-django 3.1.1
- pytest, pytest-django, pytest-cov
- django-redis 5.4.0
- PyJWT 2.8.0

---

## Virtual Environment

The scripts automatically manage a dedicated virtual environment `.venv_tests/` in the project root.

**Manual activation:**
```bash
# On macOS/Linux
source .venv_tests/bin/activate

# On Windows (Git Bash)
source .venv_tests/Scripts/activate
```

**Manual deactivation:**
```bash
deactivate
```

---

## Typical Workflows

### 1. Run All Tests (Full Suite)
```bash
./scripts/run_all_tests.sh -q
```
Runs all 5 apps, generates summary with pass/fail counts, **auto-cleans temporary files**.

### 2. Develop in App 2
```bash
./scripts/run_single_app.sh app2_mutations -v --tb=short
```
Runs only app2 tests with verbose output for debugging, **auto-cleans temporary files**.

### 3. Full Suite with Coverage Reports
```bash
./scripts/run_all_tests.sh --cov=config --cov=basics_app --cov=mutations_app
```
Generates HTML coverage reports in `htmlcov/` directories (preserved for review).

### 4. Quick Smoke Test
```bash
./scripts/run_all_tests.sh -q --tb=no
```
Fast run without detailed output for CI/CD pipelines (auto-cleanup included).

### 5. Complete Reset Between Environments
```bash
./scripts/cleanup.sh
./scripts/run_all_tests.sh
```
Full cleanup and fresh start (usually not needed since cleanup is automatic).

---

## Test Output Examples

### Successful Run
```
==========================================
Setting up virtual environment...
==========================================
✅ Virtual environment already exists
Installing dependencies...
✅ Dependencies installed

==========================================
Running tests for all apps
==========================================

Running tests for app1_basics...
------------------------------------------
✅ app1_basics passed

Running tests for app2_mutations...
------------------------------------------
✅ app2_mutations passed

==========================================
Test Summary
==========================================
Passed: 5 apps
  ✅ app1_basics
  ✅ app2_mutations
  ✅ app3_filtering
  ✅ app4_auth
  ✅ app5_performance

All apps passed! 🎉
==========================================
Cleaning up temporary files...
==========================================
✅ Cleanup complete
```

### Failed Run
```
==========================================
Test Summary
==========================================
Passed: 4 apps
  ✅ app1_basics
  ✅ app2_mutations
  ✅ app3_filtering
  ✅ app4_auth

Failed: 1 apps
  ❌ app5_performance

========================================== (Exit code: 1)
```

---

## Pytest Options Reference

Common pytest flags to pass to test scripts:

| Option | Description |
|--------|-------------|
| `-v` | Verbose output (show each test) |
| `-q` | Quiet output (minimal) |
| `-x` | Stop on first failure |
| `--tb=short` | Short traceback format |
| `--tb=no` | No traceback output |
| `--cov=MODULE` | Generate coverage for module |
| `--cov-report=html` | Generate HTML coverage report |
| `-k PATTERN` | Run only tests matching pattern |
| `--lf` | Run last failed tests only |

**Examples:**
```bash
./scripts/run_single_app.sh app1_basics -v -x --tb=short
./scripts/run_all_tests.sh -q --cov=config --cov-report=html
./scripts/run_single_app.sh app2_mutations -k test_mutation --lf
```

---

## Troubleshooting

### Virtual Environment Activation Issues
If scripts fail to activate venv, ensure bash is being used:
```bash
bash ./scripts/run_all_tests.sh
bash ./scripts/run_single_app.sh app1_basics
```

### Permission Denied
Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Dependency Installation Fails
Update pip first:
```bash
python -m pip install --upgrade pip
python -m pip install -r scripts/dev-requirements.txt
```

### Stuck Virtual Environment
Remove and recreate:
```bash
./scripts/cleanup.sh
./scripts/run_all_tests.sh
```

---

## CI/CD Integration

For automated testing pipelines (cleanup is automatic):

```yaml
# GitHub Actions example
- name: Run all tests
  run: bash scripts/run_all_tests.sh -q --tb=short

- name: Generate coverage
  run: bash scripts/run_single_app.sh app1_basics --cov --cov-report=xml
  
# No cleanup step needed - happens automatically!
```

---

## File Structure

```
scripts/
├── README.md                  # This file
├── run_all_tests.sh          # Run all apps
├── run_single_app.sh         # Run single app
├── cleanup.sh                # Manual cleanup utility
└── dev-requirements.txt      # Python dependencies

Project Root/
├── app1_basics/
├── app2_mutations/
├── app3_filtering/
├── app4_auth/
├── app5_performance/
└── .venv_tests/              # Auto-created virtual env
```

---

## Notes

- Virtual environment is **isolated** to `.venv_tests/` - safe to delete with `cleanup.sh`
- **Automatic cleanup** removes temporary files (coverage, caches) after each test run
- HTML coverage reports are **preserved** in `htmlcov/` for review
- Scripts work on macOS, Linux, and Windows (Git Bash)
- All apps are tested independently but sequentially
- Coverage files are cleaned automatically, no manual intervention needed

---

For more information, see the main [README.md](../README.md) in the project root.
