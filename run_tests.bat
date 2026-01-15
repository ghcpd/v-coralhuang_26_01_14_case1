@echo off
REM run_tests.bat - One-click test runner for FakeUserAgent mutable default fix
REM Usage: run_tests.bat

echo ============================================
echo FakeUserAgent Test Suite
echo ============================================
echo.

REM Run pytest with verbose output
python -m pytest test_fake.py -v

REM Capture the exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ============================================
if %EXIT_CODE% EQU 0 (
    echo SUCCESS: All tests passed!
) else (
    echo FAILURE: Some tests failed!
)
echo ============================================

exit /b %EXIT_CODE%
