# Survey Management App - Python 3.13.7 Setup Script

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Survey Management App - Python 3.13.7 Setup" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "Checking Python versions..." -ForegroundColor Yellow

try {
    $pythonVersions = py -0 2>&1
    Write-Host "Available Python versions:"
    Write-Host $pythonVersions
    
    if ($pythonVersions -match "3\.13") {
        Write-Host "Python 3.13 is available" -ForegroundColor Green
    } else {
        Write-Host "Python 3.13 is not installed" -ForegroundColor Red
        Write-Host "Please install Python 3.13.7 from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "Python launcher not found. Please install Python 3.13.7" -ForegroundColor Red
    exit 1
}

Write-Host "Creating virtual environment with Python 3.13..." -ForegroundColor Yellow

try {
    py -3.13 -m venv venv
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "Setting up the project..." -ForegroundColor Yellow

& ".\venv\Scripts\Activate.ps1"

Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Set-Location backend

Write-Host "Installing project dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to install some dependencies" -ForegroundColor Red
}

Set-Location ..

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Virtual environment is already activated"
Write-Host "2. Configure AWS credentials (see DYNAMODB_MIGRATION.md)"
Write-Host "3. Create DynamoDB tables: cd backend; python create_tables.py create"
Write-Host "4. Run the application: python main.py"

Write-Host "To reactivate the virtual environment later:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1"

Write-Host "To deactivate the virtual environment:" -ForegroundColor Cyan
Write-Host "  deactivate"
