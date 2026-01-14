@echo off
REM Install test dependencies and run tests (Windows)
python -m pip install -r requirements.txt
set PYTHONPATH=src
python -m pytest -q
pause