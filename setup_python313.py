#!/usr/bin/env python3
"""
Python 3.13.7 Setup Script for Survey Management App
This script helps configure the project to use Python 3.13.7
"""

import os
import sys
import subprocess
import platform

def run_command(command, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python 3.13.7 is available"""
    print("Checking Python versions...")
    
    # Check current Python version
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Current Python version: {current_version}")
    
    # On Windows, check py launcher
    if platform.system() == "Windows":
        success, output, error = run_command("py -0")
        if success:
            print("Available Python versions:")
            print(output)
            
            # Check if 3.13 is available
            if "3.13" in output:
                print("✓ Python 3.13 is available")
                return True
            else:
                print("✗ Python 3.13 is not installed")
                return False
    else:
        # On Unix-like systems, check python3.13
        success, output, error = run_command("python3.13 --version")
        if success:
            print(f"✓ Python 3.13 is available: {output.strip()}")
            return True
        else:
            print("✗ Python 3.13 is not installed")
            return False

def create_virtual_environment():
    """Create a virtual environment with Python 3.13"""
    print("\nCreating virtual environment with Python 3.13...")
    
    venv_path = "venv"
    
    if platform.system() == "Windows":
        # Use py launcher on Windows
        success, output, error = run_command(f"py -3.13 -m venv {venv_path}")
    else:
        # Use python3.13 on Unix-like systems
        success, output, error = run_command(f"python3.13 -m venv {venv_path}")
    
    if success:
        print(f"✓ Virtual environment created at {venv_path}")
        return True
    else:
        print(f"✗ Failed to create virtual environment: {error}")
        return False

def activate_virtual_environment():
    """Provide instructions for activating the virtual environment"""
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("  PowerShell: .\\venv\\Scripts\\Activate.ps1")
        print("  Command Prompt: venv\\Scripts\\activate.bat")
    else:
        print("  source venv/bin/activate")

def install_dependencies():
    """Install project dependencies"""
    print("\nAfter activating the virtual environment, install dependencies:")
    print("  cd backend")
    print("  pip install --upgrade pip")
    print("  pip install -r requirements.txt")

def setup_project():
    """Main setup function"""
    print("=" * 60)
    print("Survey Management App - Python 3.13.7 Setup")
    print("=" * 60)
    
    # Check if Python 3.13 is available
    if not check_python_version():
        print("\nPlease install Python 3.13.7 from:")
        print("https://www.python.org/downloads/")
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Provide activation instructions
    activate_virtual_environment()
    
    # Provide dependency installation instructions
    install_dependencies()
    
    print("\n" + "=" * 60)
    print("Setup complete! Next steps:")
    print("1. Activate the virtual environment (see commands above)")
    print("2. Navigate to backend directory: cd backend")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Configure AWS credentials (see DYNAMODB_MIGRATION.md)")
    print("5. Create DynamoDB tables: python create_tables.py create")
    print("6. Run the application: python main.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)