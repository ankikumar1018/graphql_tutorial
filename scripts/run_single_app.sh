#!/bin/bash

# Run tests for a single app with virtual environment
# Usage: ./run_single_app.sh app_name [options]
# Example: ./run_single_app.sh app1_basics -v --cov=basics_app

if [ $# -lt 1 ]; then
    echo "Usage: $0 <app_name> [pytest_options]"
    echo ""
    echo "Available apps:"
    echo "  - app1_basics"
    echo "  - app2_mutations"
    echo "  - app3_filtering"
    echo "  - app4_auth"
    echo "  - app5_performance"
    echo ""
    echo "Examples:"
    echo "  $0 app1_basics"
    echo "  $0 app1_basics -v"
    echo "  $0 app1_basics --cov=basics_app"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv_tests"

APP_NAME="$1"
shift  # Remove first argument, pass rest to pytest

APP_PATH="$PROJECT_ROOT/$APP_NAME"

# Trap to cleanup on exit
trap cleanup EXIT
cleanup() {
    echo ""
    echo "========================================="
    echo "Cleaning up temporary files..."
    echo "========================================="
    
    # Remove coverage files
    find "$PROJECT_ROOT" -type f -name ".coverage*" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "coverage.xml" -delete 2>/dev/null || true
    
    # Remove pytest cache
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    
    echo "✅ Cleanup complete"
}

if [ ! -d "$APP_PATH" ]; then
    echo "❌ Error: App '$APP_NAME' not found at $APP_PATH"
    exit 1
fi

# Setup virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Install dependencies
pip install -q -r "$SCRIPT_DIR/dev-requirements.txt"

echo "Running tests for $APP_NAME..."
echo "=========================================="

cd "$APP_PATH"
pytest tests/ "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ $APP_NAME tests passed"
else
    echo "❌ $APP_NAME tests failed"
fi

exit $EXIT_CODE
