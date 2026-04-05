@echo off
REM Try to find OpenModelica bin directory
if exist "C:\OpenModelica\bin" (
    SET PATH=C:\OpenModelica\bin;%PATH%
) else if exist "D:\Harish Kumar\bin" (
    SET PATH=D:\Harish Kumar\bin;%PATH%
)

SET ERRORLEVEL=
CALL "%CD%/TwoConnectedTanks.exe" %*
SET RESULT=%ERRORLEVEL%

EXIT /b %RESULT%
