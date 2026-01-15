@echo off
python -m pytest -q %*
exit /b %ERRORLEVEL%
