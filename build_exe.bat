@echo off
REM build_exe.bat - Convert Python application to standalone .exe
REM This creates a single executable file that can be distributed without Python
REM
REM Requirements:
REM   - Python 3.8+ installed
REM   - Virtual environment with dependencies
REM   - PyInstaller (installed automatically)
REM
REM Output:
REM   - dist/OpenModelica Simulator.exe (standalone executable)

echo.
echo ========================================
echo Building OpenModelica Simulator EXE
echo ========================================
echo.
echo This may take a few moments...
echo.

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Kill any running instance of the previous exe
echo [1/6] Cleaning up previous instances...
taskkill /IM "OpenModelica Simulator.exe" /F >nul 2>&1
taskkill /IM "launcher.exe" /F >nul 2>&1
timeout /t 2 /nobreak >nul 2>&1

REM Check if virtual environment exists
if not exist ".venv\" (
    echo [2/6] Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo [3/6] Installing dependencies...
pip install -q -r requirements.txt
if !errorlevel! neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller
echo [4/6] Installing PyInstaller...
pip install -q pyinstaller
if !errorlevel! neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Clean previous builds
if exist "build\" rmdir /s /q "build\" >nul 2>&1
if exist "dist\" rmdir /s /q "dist\" >nul 2>&1
if exist "__pycache__\" rmdir /s /q "__pycache__\" >nul 2>&1
if exist "src\__pycache__\" rmdir /s /q "src\__pycache__\" >nul 2>&1
if exist ".spec" del /q "*.spec" >nul 2>&1

REM Build the executable
echo [5/6] Building executable...
echo        (Using launcher.py as entry point with splash screen)
echo.

REM PyInstaller configuration:
REM   --onefile:             Single executable file (not directory)
REM   --windowed:            No console window (GUI-only)
REM   --name:                Output filename
REM   --add-data:            Include data files/directories (src;src adds src/ dir)
REM   --hidden-import:       Force PyInstaller to include modules
REM   --collect-all:         Collect entire package and submodules
REM   --distpath:            Output directory for executable
REM   --specpath:            Where to write the .spec file

REM Build executable directly from app.py (not launcher)
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "OpenModelica Simulator" ^
    --add-data "src;src" ^
    --add-data "model;model" ^
    --collect-all PyQt6 ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PyQt6.QtGui ^
    --distpath=dist ^
    --specpath=. ^
    --icon=NONE ^
    src\app.py

if !errorlevel! neq 0 (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Possible solutions:
    echo   1. Kill running instances: taskkill /IM "OpenModelica Simulator.exe" /F
    echo   2. Check dependencies: pip install -r requirements.txt
    echo   3. Verify Python 3.8+: python --version
    echo   4. Clear cache: rmdir /s /q build __pycache__ src\__pycache__
    echo   5. Reinstall: pip install --upgrade pyinstaller PyQt6
    echo   6. Check file permissions on src/ and model/
    echo.
    pause
    exit /b 1
)

echo [6/6] Verifying executable...

if not exist "dist\OpenModelica Simulator.exe" (
    echo ERROR: Executable was not created!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your executable is ready at:
echo   dist\OpenModelica Simulator.exe
echo.
echo Next steps:
echo   1. Run the executable: dist\OpenModelica Simulator.exe
echo   2. Create a shortcut on desktop for easy access
echo   3. Distribute to others (no Python installation needed)
echo.
echo Note: First launch may take a few seconds to extract bundled files
echo.
pause
