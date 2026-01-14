@echo off
REM Install test requirements then run pytest
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
python -m pytest -q
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%