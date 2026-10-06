@echo off
setlocal

if "%~1"=="" (
    echo Please drag a Tupperbox JSON export onto this file.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo Error: The specified file could not be found.
    pause
    exit /b 1
)

python "%~dp0tupper_viewer.py" "%~1"

if errorlevel 1 (
    echo.
    echo The program exited with an error.
    pause
)

endlocal
