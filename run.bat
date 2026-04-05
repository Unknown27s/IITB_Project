@echo off
REM Simple launcher for OpenModelica GUI
setlocal enabledelayedexpansion

if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Starting OpenModelica Model Simulator
echo ========================================
echo.

python src/app.py

if !errorlevel! neq 0 (
    echo.
    echo ========================================
    echo ERROR: Application crashed!
    echo ========================================
    echo Check error_log.txt for details.
    echo.
    pause
)

