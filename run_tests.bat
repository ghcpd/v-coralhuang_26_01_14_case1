@echo off
REM Windows Test Runner Script for fake-useragent
REM This script installs dependencies and runs all tests

echo.
echo ================================================
echo fake-useragent Test Runner
echo ================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python is available
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and ensure it's added to your PATH
    exit /b 1
)

python --version

REM Check if pip is available
echo.
echo Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    exit /b 1
)

REM Create/verify requirements.txt
echo.
echo Creating requirements.txt if needed...
(
    echo pytest
    echo pytest-cov
) > requirements.txt

REM Install dependencies
echo.
echo Installing test dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo Dependencies installed successfully!

REM Run tests
echo.
echo ================================================
echo Running Tests
echo ================================================
echo.

REM Change to src directory where test modules are located
cd src
python -m pytest test_fake.py -v
set TEST_RESULT=%errorlevel%
cd ..

REM Capture exit code
if %TEST_RESULT% neq 0 (
    echo.
    echo ================================================
    echo TEST EXECUTION FAILED
    echo ================================================
    exit /b 1
) else (
    echo.
    echo ================================================
    echo ALL TESTS PASSED!
    echo ================================================
    exit /b 0
)
