#!/bin/bash

# Run all GraphQL Django app tests with virtual environment
# Usage: ./run_all_tests.sh [options]
# Options: -q (quiet), --tb=short/no, --cov (coverage), etc.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv_tests"

APPS=("app1_basics" "app2_mutations" "app3_filtering" "app4_auth" "app5_performance")

# Trap to cleanup on exit
trap cleanup EXIT
cleanup() {
    echo ""
    echo "=========================================="
    echo "Cleaning up temporary files..."
    echo "=========================================="
    
    # Remove coverage files
    find "$PROJECT_ROOT" -type f -name ".coverage*" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "coverage.xml" -delete 2>/dev/null || true
    
    # Remove pytest cache
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    
    echo "✅ Cleanup complete"
}

# Setup virtual environment
echo "=========================================="
echo "Setting up virtual environment..."
echo "=========================================="

if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    python -m venv "$VENV_PATH"
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install -q -r "$SCRIPT_DIR/dev-requirements.txt"
echo "✅ Dependencies installed"

echo "=========================================="
echo "Running tests for all apps"
echo "=========================================="

FAILED_APPS=()
PASSED_APPS=()
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
APP_RESULTS=()

for app in "${APPS[@]}"; do
    APP_PATH="$PROJECT_ROOT/$app"
    
    if [ ! -d "$APP_PATH" ]; then
        echo "❌ $app not found at $APP_PATH"
        FAILED_APPS+=("$app")
        continue
    fi
    
    echo ""
    echo "Running tests for $app..."
    echo "------------------------------------------"
    
    cd "$APP_PATH"
    
    # Capture pytest output to extract statistics
    PYTEST_OUTPUT=$(pytest tests/ "$@" 2>&1)
    PYTEST_EXIT=$?
    echo "$PYTEST_OUTPUT"
    
    # Extract test counts from output (passed/failed test counts, not coverage)
    if [[ $PYTEST_OUTPUT =~ ([0-9]+)\ passed ]]; then
        PASSED_COUNT="${BASH_REMATCH[1]}"
        TOTAL_PASSED=$((TOTAL_PASSED + PASSED_COUNT))
    else
        PASSED_COUNT=0
    fi
    
    # Check if there are failed tests (not coverage failures)
    if [[ $PYTEST_OUTPUT =~ ([0-9]+)\ failed ]]; then
        FAILED_COUNT="${BASH_REMATCH[1]}"
        TOTAL_FAILED=$((TOTAL_FAILED + FAILED_COUNT))
    else
        FAILED_COUNT=0
    fi
    
    APP_TOTAL=$((PASSED_COUNT + FAILED_COUNT))
    if [ $APP_TOTAL -gt 0 ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + APP_TOTAL))
        APP_RESULTS+=("$app: $PASSED_COUNT/$APP_TOTAL passed")
    fi
    
    # Determine if app tests passed: passed tests exist and no actual test failures
    if [ $PASSED_COUNT -gt 0 ] && [ $FAILED_COUNT -eq 0 ]; then
        echo "✅ $app passed ($PASSED_COUNT tests)"
        PASSED_APPS+=("$app")
    else
        echo "❌ $app failed ($FAILED_COUNT test failures)"
        FAILED_APPS+=("$app")
    fi
done

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total Tests Run: $TOTAL_TESTS"
echo "Total Passed: $TOTAL_PASSED"
echo "Total Failed: $TOTAL_FAILED"
echo ""
echo "Per App Results:"
for result in "${APP_RESULTS[@]}"; do
    echo "  $result"
done

echo ""
echo "Apps Summary:"
echo "Passed Apps: ${#PASSED_APPS[@]} apps"
for app in "${PASSED_APPS[@]}"; do
    echo "  ✅ $app"
done

if [ ${#FAILED_APPS[@]} -gt 0 ]; then
    echo "Failed Apps: ${#FAILED_APPS[@]} apps"
    for app in "${FAILED_APPS[@]}"; do
        echo "  ❌ $app"
    done
    echo ""
    echo "❌ Some tests failed. See details above."
    exit 1
else
    echo "✅ All apps passed!"
    exit 0
fi
