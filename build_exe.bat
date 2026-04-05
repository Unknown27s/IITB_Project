@echo off
REM build_exe.bat - Convert Python launcher to standalone .exe
REM This creates a single executable file that can be distributed

echo.
echo ========================================
echo Building OpenModelica Simulator EXE
echo ========================================
echo.

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install PyInstaller
echo Installing PyInstaller...
pip install -q pyinstaller

REM Build the executable
echo Building executable...
pyinstaller --onefile --windowed --name "OpenModelica Simulator" --add-data "src:src" --add-data "model:model" --add-data "requirements.txt:." launcher.py

if !errorlevel! neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your executable is ready:
echo   dist\OpenModelica Simulator.exe
echo.
echo You can now:
echo   1. Run it directly by double-clicking
echo   2. Create a shortcut for easy access
echo   3. Distribute it to others
echo.
pause
