#!/bin/bash

# Cleanup script for GraphQL Django test environment
# Removes virtual environment, cache files, and coverage reports

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Cleaning up test environment..."
echo "=========================================="

# Remove virtual environment
if [ -d "$PROJECT_ROOT/.venv_tests" ]; then
    echo "Removing virtual environment (.venv_tests)..."
    rm -rf "$PROJECT_ROOT/.venv_tests"
    echo "✅ Virtual environment removed"
else
    echo "⚠️  Virtual environment not found"
fi

# Remove coverage files
echo "Removing coverage files..."
find "$PROJECT_ROOT" -type f -name ".coverage*" -delete
find "$PROJECT_ROOT" -type f -name "coverage.xml" -delete
echo "✅ Coverage files removed"

# Remove pytest cache
echo "Removing pytest cache..."
find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo "✅ Pytest cache removed"

# Remove htmlcov directories
echo "Removing HTML coverage reports..."
find "$PROJECT_ROOT" -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
echo "✅ HTML coverage reports removed"

echo ""
echo "=========================================="
echo "Cleanup complete! 🎉"
