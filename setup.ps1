# Survey Management Application - PowerShell Setup Script

Write-Host "🚀 Survey Management Application - Advanced Setup" -ForegroundColor Green
Write-Host ""

# Function to test if a command exists
function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to test Python properly (avoiding Microsoft Store stub)
function Test-Python() {
    try {
        $pythonPath = Get-Command python -ErrorAction SilentlyContinue
        if ($pythonPath -and $pythonPath.Source -notlike "*WindowsApps*") {
            $version = & python --version 2>&1
            if ($version -match "Python \d+\.\d+\.\d+") {
                return $true
            }
        }
        
        # Try py launcher
        $pyPath = Get-Command py -ErrorAction SilentlyContinue
        if ($pyPath) {
            $version = & py --version 2>&1
            if ($version -match "Python \d+\.\d+\.\d+") {
                return $true
            }
        }
        
        return $false
    }
    catch {
        return $false
    }
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
if (Test-Python) {
    Write-Host "✅ Python found" -ForegroundColor Green
    $pythonCmd = "python"
    
    # Use py launcher if python is Microsoft Store stub
    $pythonPath = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonPath.Source -like "*WindowsApps*") {
        $pythonCmd = "py"
        Write-Host "   Using py launcher to avoid Microsoft Store stub" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Python not found or not properly configured" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python manually:" -ForegroundColor Yellow
    Write-Host "1. Go to https://www.python.org/downloads/"
    Write-Host "2. Download Python 3.8+ (recommend 3.12)"
    Write-Host "3. During installation, CHECK 'Add Python to PATH'"
    Write-Host "4. Restart PowerShell and run this script again"
    Write-Host ""
    Write-Host "Or try: winget install Python.Python.3.12" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
if (Test-Command "node") {
    Write-Host "✅ Node.js found" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js manually:" -ForegroundColor Yellow
    Write-Host "1. Go to https://nodejs.org/"
    Write-Host "2. Download the LTS version"
    Write-Host "3. Install with default settings"
    Write-Host "4. Restart PowerShell and run this script again"
    Write-Host ""
    Write-Host "Or try: winget install OpenJS.NodeJS" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📦 Setting up Python backend..." -ForegroundColor Blue

# Navigate to backend
Set-Location backend

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
& $pythonCmd -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
& ".\venv\Scripts\pip.exe" install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Backend setup complete!" -ForegroundColor Green

# Frontend setup
Write-Host ""
Write-Host "📦 Setting up React frontend..." -ForegroundColor Blue
Set-Location ..\frontend

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Node.js dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Frontend setup complete!" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure your database connection in backend\.env"
Write-Host "2. Run the database schema from Database Scripts\schema.sql"
Write-Host "3. Start the backend: cd backend; .\venv\Scripts\Activate.ps1; uvicorn main:app --reload"
Write-Host "4. Start the frontend: cd frontend; npm start"
Write-Host ""

Read-Host "Press Enter to exit"
