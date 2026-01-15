@echo off
REM Test runner for FakeUserAgent project
REM This script runs all tests and reports results

echo ========================================
echo Running FakeUserAgent Test Suite
echo ========================================
echo.

REM Check if pytest is available
python -m pytest --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pytest is not installed
    echo Please install it with: pip install pytest
    exit /b 1
)

REM Run tests with verbose output
echo Running tests...
echo.
python -m pytest test_fake.py -v --tb=short

REM Check the result
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS: All tests passed!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo FAILURE: Some tests failed!
    echo ========================================
    exit /b 1
)

exit /b 0
