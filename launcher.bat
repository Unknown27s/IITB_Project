@echo off
REM OpenModelica Simulator - Quick Launcher
REM Simple wrapper to start the application

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies silently
pip install -q -r requirements.txt

REM Launch the launcher
python launcher.py

pause
