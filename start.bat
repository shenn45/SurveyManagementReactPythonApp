@echo off
echo 🚀 Starting Survey Management Application...

echo.
echo Starting Backend (FastAPI)...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend (React)...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both servers are starting...
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause >nul
