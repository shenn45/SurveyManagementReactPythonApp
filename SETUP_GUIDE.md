# 🚀 Survey Management Application Setup Guide

## Current Status
The project structure is complete, but we need to install Python and Node.js to run the setup scripts.

## Prerequisites Installation

### Step 1: Install Python 3.8+

**Option A: Using Windows Package Manager (Recommended)**
1. Open PowerShell as Administrator (Right-click PowerShell → "Run as Administrator")
2. Run: `winget install Python.Python.3.12`
3. Close and restart your regular PowerShell

**Option B: Manual Download**
1. Go to https://www.python.org/downloads/
2. Download Python 3.12 (latest stable)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Restart your terminal

### Step 2: Install Node.js 16+

**Option A: Using Windows Package Manager**
1. In Administrator PowerShell: `winget install OpenJS.NodeJS`
2. Restart your terminal

**Option B: Manual Download**
1. Go to https://nodejs.org/
2. Download the LTS version
3. Run the installer (automatically adds to PATH)
4. Restart your terminal

### Step 3: Verify Installation

Open a new PowerShell window and verify:
```powershell
python --version
node --version
npm --version
```

### Step 4: Run Setup Script

Once both are installed, run our setup script:
```powershell
.\setup.ps1
```

## Quick Install Commands (Run as Administrator)

```powershell
# Install both prerequisites
winget install Python.Python.3.12
winget install OpenJS.NodeJS

# Restart PowerShell, then run:
.\setup.ps1
```

## What the Setup Script Does

1. **Backend Setup:**
   - Creates Python virtual environment
   - Installs FastAPI and dependencies
   - Sets up database models and API routes

2. **Frontend Setup:**
   - Installs React and TypeScript
   - Installs TailwindCSS and HeadlessUI
   - Sets up routing and components

## After Successful Setup

### 1. Configure Database Connection
Copy `backend\.env.example` to `backend\.env` and update:
```
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

### 2. Run Database Schema
Execute the SQL script in `Database Scripts\schema.sql` in your SQL Server

### 3. Start the Applications

**Backend (Terminal 1):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```
API will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

**Frontend (Terminal 2):**
```powershell
cd frontend
npm start
```
React app will be available at: http://localhost:3000

## Troubleshooting

### Python Issues
- If you see "Python was not found", the Microsoft Store stub is interfering
- Try using `py` instead of `python`
- Disable Python app execution aliases in Windows Settings

### Node.js Issues
- Restart terminal after installation
- Verify with `node --version` and `npm --version`

### Permission Issues
- Run PowerShell as Administrator for installations
- Set execution policy: `Set-ExecutionPolicy RemoteSigned`

## Project Features Ready to Use

✅ **Complete API Backend**
- Customer CRUD operations
- Survey management endpoints
- Property management
- Database relationships
- Search and pagination

✅ **Modern React Frontend**
- Customer management interface
- Responsive design with TailwindCSS
- Modal forms and data tables
- Search and pagination
- TypeScript for type safety

✅ **Development Ready**
- Hot reload for both backend and frontend
- Comprehensive error handling
- API documentation
- Development and production configurations
