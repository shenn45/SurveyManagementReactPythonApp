#!/usr/bin/env python3
"""
Test runner script for Survey Management App
Provides comprehensive testing with coverage reports
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description or command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Exit code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def setup_environment():
    """Setup test environment"""
    print("Setting up test environment...")
    
    # Ensure we're in the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print("Warning: No virtual environment detected!")
        print("Please activate your virtual environment first:")
        print("  .\\venv\\Scripts\\Activate.ps1  # Windows")
        print("  source venv/bin/activate      # Linux/Mac")
        return False
    
    return True


def run_unit_tests():
    """Run unit tests"""
    return run_command(
        "pytest tests/unit/ -v --tb=short",
        "Unit Tests"
    )


def run_integration_tests():
    """Run integration tests"""
    return run_command(
        "pytest tests/integration/ -v --tb=short",
        "Integration Tests"
    )


def run_all_tests():
    """Run all tests with coverage"""
    return run_command(
        "pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov --cov-exclude='venv/*' --cov-exclude='tests/*' --cov-fail-under=80",
        "All Tests with Coverage"
    )


def run_specific_tests(pattern):
    """Run tests matching a specific pattern"""
    return run_command(
        f"pytest tests/ -v -k '{pattern}' --tb=short",
        f"Tests matching pattern: {pattern}"
    )


def generate_coverage_report():
    """Generate detailed coverage report"""
    print("\nGenerating coverage report...")
    run_command("coverage report --show-missing", "Coverage Report")
    run_command("coverage html", "HTML Coverage Report")
    print("\nHTML coverage report generated in: htmlcov/index.html")


def lint_code():
    """Run code linting"""
    print("\nRunning code quality checks...")
    
    # Check if flake8 is installed, if not skip
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        run_command("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Critical Lint Issues")
        run_command("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics", "All Lint Issues")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Flake8 not installed, skipping lint checks")


def check_test_files():
    """Check that all test files are present"""
    print("\nChecking test file structure...")
    
    expected_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/unit/__init__.py",
        "tests/unit/test_models.py",
        "tests/unit/test_database.py",
        "tests/unit/test_crud.py",
        "tests/integration/__init__.py",
        "tests/integration/test_api_endpoints.py",
        "tests/integration/test_graphql.py",
        "pytest.ini"
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("Missing test files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✓ All test files present")
        return True


def main():
    """Main test runner function"""
    if not setup_environment():
        sys.exit(1)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Test runner for Survey Management App")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--coverage", action="store_true", help="Run all tests with coverage")
    parser.add_argument("--pattern", help="Run tests matching pattern")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--check", action="store_true", help="Check test file structure")
    parser.add_argument("--all", action="store_true", help="Run everything (default)")
    
    args = parser.parse_args()
    
    # If no specific options, run all
    if not any([args.unit, args.integration, args.coverage, args.pattern, args.lint, args.check]):
        args.all = True
    
    success = True
    
    # Check test file structure
    if args.check or args.all:
        if not check_test_files():
            success = False
    
    # Run linting
    if args.lint or args.all:
        lint_code()
    
    # Run specific test categories
    if args.unit:
        success &= run_unit_tests()
    
    if args.integration:
        success &= run_integration_tests()
    
    if args.coverage or args.all:
        success &= run_all_tests()
        generate_coverage_report()
    
    if args.pattern:
        success &= run_specific_tests(args.pattern)
    
    # Summary
    print("\n" + "="*60)
    if success:
        print("✓ All tests completed successfully!")
        print("\nNext steps:")
        print("1. Review coverage report: htmlcov/index.html")
        print("2. Check for any failing tests and fix them")
        print("3. Ensure coverage is above 80%")
        sys.exit(0)
    else:
        print("✗ Some tests failed or errors occurred")
        print("\nPlease review the output above and fix any issues")
        sys.exit(1)


if __name__ == "__main__":
    main()