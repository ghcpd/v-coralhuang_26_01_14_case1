@echo off
REM Install test deps and run pytest
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt >nul
python -m pytest -q
