@echo off
echo 🚀 Survey Management Application - Advanced Setup

echo.
echo Checking prerequisites...

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found or not properly configured
    echo.
    echo Please install Python manually:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.8+ (recommend 3.12)
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Restart this terminal and run setup again
    echo.
    echo Or try: winget install Python.Python.3.12
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

REM Check for Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found
    echo.
    echo Please install Node.js manually:
    echo 1. Go to https://nodejs.org/
    echo 2. Download the LTS version
    echo 3. Install with default settings
    echo 4. Restart this terminal and run setup again
    echo.
    echo Or try: winget install OpenJS.NodeJS
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
)

echo.
echo 📦 Setting up Python backend...
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete!

REM Frontend setup
echo.
echo 📦 Setting up React frontend...
cd ..\frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend setup complete!

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Configure your database connection in backend\.env
echo 2. Run the database schema from Database Scripts\schema.sql
echo 3. Start the backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo 4. Start the frontend: cd frontend ^&^& npm start
echo.

pause
