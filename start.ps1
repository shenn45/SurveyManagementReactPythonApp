# Survey Management Application - Start Script

Write-Host "🚀 Starting Survey Management Application..." -ForegroundColor Green
Write-Host ""

# Check if setup has been completed
if (-not (Test-Path "backend\venv\Scripts\python.exe")) {
    Write-Host "❌ Backend not set up. Please run setup.ps1 first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Frontend not set up. Please run setup.ps1 first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; uvicorn main:app --reload"

Start-Sleep -Seconds 3

Write-Host "Starting Frontend (React)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"

Write-Host ""
Write-Host "✅ Both servers are starting..." -ForegroundColor Green
Write-Host ""
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Yellow
Write-Host "API Documentation at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to close this window"
