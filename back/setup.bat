@echo off
echo ====================================
echo MedSite Backend Setup Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Checking Python version...
python --version
echo.

REM Remove old virtual environment if exists
if exist .venv (
    echo Step 2: Removing old virtual environment...
    rmdir /s /q .venv
    echo Old virtual environment removed.
    echo.
)

REM Create new virtual environment
echo Step 3: Creating new virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

REM Activate virtual environment
echo Step 4: Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Upgrade pip
echo Step 5: Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Step 6: Installing dependencies...
pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying individual package installation...
    pip install fastapi[standard]
    pip install uvicorn[standard]
    pip install sqlalchemy
    pip install sqlmodel
    pip install "python-jose[cryptography]"
    pip install "passlib[bcrypt]"
    pip install bcrypt
    pip install python-multipart
    pip install python-dotenv
    pip install cryptography
)
echo.

REM Verify installations
echo Step 7: Verifying installations...
pip list | findstr /i "fastapi uvicorn sqlmodel passlib jose bcrypt"
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To run the server:
echo 1. Make sure virtual environment is activated: .venv\Scripts\activate
echo 2. Run: uvicorn main:app --reload
echo.
echo The API will be available at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.
pause