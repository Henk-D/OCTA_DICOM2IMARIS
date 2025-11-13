@echo off
chcp 65001 >nul
REM Launch OCTA Converter GUI

python "%~dp0OCTA_Converter_GUI.py"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to launch GUI!
    echo.
    echo Please check:
    echo   1. Python is installed
    echo   2. Required packages are installed: pip install -r requirements.txt
    echo   3. Or setup conda environment: setup_environment.bat
    echo.
    pause
)
