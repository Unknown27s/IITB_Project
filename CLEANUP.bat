@echo off
REM Cleanup unnecessary files - keep only what's needed for standalone version
REM Run this script to clean up your project directory

echo.
echo ========================================
echo Cleaning up project directory...
echo ========================================
echo.

REM Files to DELETE (optional docs, cache, etc)
echo Removing unnecessary documentation files...
del /Q README_AI_DEVELOPMENT.md 2>nul
del /Q LAUNCHER_GUIDE.md 2>nul
del /Q DISTRIBUTION_GUIDE.md 2>nul
del /Q PROJECT_COMPLETION.md 2>nul

echo Removing unnecessary files...
del /Q SUBMISSION.py 2>nul
del /Q run.sh 2>nul
del /Q OpenModelica\ Simulator.spec 2>nul
del /Q error_log.txt 2>nul

REM Clean Python cache
echo Removing Python cache...
rmdir /S /Q __pycache__ 2>nul
rmdir /S /Q build 2>nul
cd src && rmdir /S /Q __pycache__ 2>nul && cd ..

echo.
echo ========================================
echo BEFORE BUILDING EXE - Run these files:
echo ========================================
echo.
echo 1. Double-click: launcher.bat
echo    (Test the launcher works)
echo.
echo 2. Then run: build_exe.bat
echo    (Creates standalone .exe)
echo.
echo 3. Find at: dist/OpenModelica Simulator.exe
echo.
echo ========================================
echo CLEAN FILE STRUCTURE:
echo ========================================
echo.
echo Essential Files (Keep):
echo - src/app.py
echo - launcher.py
echo - launcher.bat
echo - run.bat
echo - build_exe.bat
echo - view_results.py
echo - requirements.txt
echo - README.md (single file!)
echo.
echo Model Folder (Keep):
echo - model/TwoConnectedTanks.exe
echo - model/TwoConnectedTanks.bat
echo - model/TwoConnectedTanks_init.xml
echo - model/TwoConnectedTanks_info.json
echo.
echo Generated later (Keep):
echo - dist/OpenModelica Simulator.exe (after build_exe.bat)
echo.
echo ========================================
echo Cleanup complete!
echo Your project is now clean and minimal.
echo ========================================
echo.

pause
