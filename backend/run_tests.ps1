# PowerShell test runner script for Windows
# Survey Management App Test Runner

param(
    [switch]$Unit,
    [switch]$Integration,
    [switch]$Coverage,
    [switch]$Lint,
    [switch]$Check,
    [string]$Pattern,
    [switch]$All,
    [switch]$Help
)

function Show-Help {
    Write-Host "Survey Management App Test Runner" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_tests.ps1 [OPTIONS]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Unit          Run only unit tests"
    Write-Host "  -Integration   Run only integration tests"
    Write-Host "  -Coverage      Run all tests with coverage report"
    Write-Host "  -Lint          Run code linting checks"
    Write-Host "  -Check         Check test file structure"
    Write-Host "  -Pattern <p>   Run tests matching pattern"
    Write-Host "  -All           Run everything (default)"
    Write-Host "  -Help          Show this help message"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\run_tests.ps1                    # Run all tests"
    Write-Host "  .\run_tests.ps1 -Unit              # Run only unit tests"
    Write-Host "  .\run_tests.ps1 -Coverage          # Run with coverage"
    Write-Host "  .\run_tests.ps1 -Pattern customer  # Run customer tests"
}

function Test-Environment {
    Write-Host "Checking test environment..." -ForegroundColor Yellow
    
    # Check if virtual environment is activated
    if (-not $env:VIRTUAL_ENV) {
        Write-Host "Error: No virtual environment detected!" -ForegroundColor Red
        Write-Host "Please activate your virtual environment first:" -ForegroundColor Yellow
        Write-Host "  .\venv\Scripts\Activate.ps1"
        return $false
    }
    
    # Check if pytest is installed
    try {
        python -m pytest --version | Out-Null
        Write-Host "✓ pytest is available" -ForegroundColor Green
    } catch {
        Write-Host "Error: pytest not installed!" -ForegroundColor Red
        Write-Host "Install it with: pip install pytest" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Invoke-TestCommand {
    param(
        [string]$Command,
        [string]$Description
    )
    
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host $Description -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $Description completed successfully" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ $Description failed with exit code $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ Error running $Description`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-FileStructure {
    Write-Host "Checking test file structure..." -ForegroundColor Yellow
    
    $expectedFiles = @(
        "tests\__init__.py",
        "tests\conftest.py",
        "tests\unit\__init__.py",
        "tests\unit\test_models.py",
        "tests\unit\test_database.py",
        "tests\unit\test_crud.py",
        "tests\integration\__init__.py",
        "tests\integration\test_api_endpoints.py",
        "tests\integration\test_graphql.py",
        "pytest.ini"
    )
    
    $missingFiles = @()
    foreach ($file in $expectedFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Host "Missing test files:" -ForegroundColor Red
        foreach ($file in $missingFiles) {
            Write-Host "  - $file" -ForegroundColor Red
        }
        return $false
    } else {
        Write-Host "✓ All test files present" -ForegroundColor Green
        return $true
    }
}

# Show help if requested
if ($Help) {
    Show-Help
    exit 0
}

# If no specific options, run all
if (-not ($Unit -or $Integration -or $Coverage -or $Lint -or $Check -or $Pattern)) {
    $All = $true
}

# Check environment first
if (-not (Test-Environment)) {
    exit 1
}

$success = $true

# Check test file structure
if ($Check -or $All) {
    if (-not (Test-FileStructure)) {
        $success = $false
    }
}

# Run linting
if ($Lint -or $All) {
    Write-Host "Running code quality checks..." -ForegroundColor Yellow
    try {
        python -m flake8 --version | Out-Null
        $success = $success -and (Invoke-TestCommand "python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics" "Critical Lint Issues")
        Invoke-TestCommand "python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics" "All Lint Issues"
    } catch {
        Write-Host "Flake8 not installed, skipping lint checks" -ForegroundColor Yellow
    }
}

# Run specific test categories
if ($Unit) {
    $success = $success -and (Invoke-TestCommand "python -m pytest tests\unit\ -v --tb=short" "Unit Tests")
}

if ($Integration) {
    $success = $success -and (Invoke-TestCommand "python -m pytest tests\integration\ -v --tb=short" "Integration Tests")
}

if ($Coverage -or $All) {
    $success = $success -and (Invoke-TestCommand "python -m pytest tests\ -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov --cov-exclude='venv/*' --cov-exclude='tests/*' --cov-fail-under=80" "All Tests with Coverage")
    
    Write-Host ""
    Write-Host "Generating detailed coverage report..." -ForegroundColor Yellow
    Invoke-TestCommand "python -m coverage report --show-missing" "Coverage Report"
    Invoke-TestCommand "python -m coverage html" "HTML Coverage Report"
    Write-Host "HTML coverage report generated in: htmlcov\index.html" -ForegroundColor Green
}

if ($Pattern) {
    $success = $success -and (Invoke-TestCommand "python -m pytest tests\ -v -k '$Pattern' --tb=short" "Tests matching pattern: $Pattern")
}

# Summary
Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Cyan
if ($success) {
    Write-Host "✓ All tests completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Review coverage report: htmlcov\index.html"
    Write-Host "2. Check for any failing tests and fix them"
    Write-Host "3. Ensure coverage is above 80%"
    exit 0
} else {
    Write-Host "✗ Some tests failed or errors occurred" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review the output above and fix any issues" -ForegroundColor Yellow
    exit 1
}