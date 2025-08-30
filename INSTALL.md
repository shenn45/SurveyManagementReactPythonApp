# Prerequisites Installation Guide

## Automatic Installation (Recommended)

### Option 1: Using Windows Package Manager (winget)

Open PowerShell as Administrator and run:

```powershell
# Install Python
winget install Python.Python.3.12

# Install Node.js
winget install OpenJS.NodeJS

# Restart your terminal or run:
refreshenv
```

### Option 2: Using Chocolatey

If you have Chocolatey installed:

```powershell
# Install Python
choco install python

# Install Node.js
choco install nodejs

# Restart your terminal
```

## Manual Installation

### Install Python 3.8+

1. Go to https://www.python.org/downloads/
2. Download Python 3.12 (latest stable version)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Verify installation: `python --version`

### Install Node.js 16+

1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer (it will automatically add to PATH)
4. Verify installation: `node --version` and `npm --version`

## After Installing Prerequisites

Once Python and Node.js are installed, run the setup script:

### Windows:
```cmd
setup.bat
```

### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

## Manual Setup (if scripts don't work)

### Backend Setup:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Frontend Setup:
```bash
cd frontend
npm install
```

## Troubleshooting

### Python not found after installation:
- Restart your terminal/PowerShell
- Check if Python is in your PATH: `echo $env:PATH` (PowerShell)
- Try using `py` instead of `python`

### npm not found after Node.js installation:
- Restart your terminal
- Verify Node.js installation: `node --version`
- Check npm: `npm --version`

### Permission errors:
- Run PowerShell as Administrator
- On Windows, you might need to run: `Set-ExecutionPolicy RemoteSigned`
