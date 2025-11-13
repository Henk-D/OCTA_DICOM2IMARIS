@echo off
chcp 65001 >nul
REM Create and setup Mamba/Conda environment for OCTA Converter

echo ================================================================================
echo Zeiss OCTA Converter - Environment Setup
echo ================================================================================
echo.
echo This script will create a conda/mamba environment with all dependencies.
echo.
echo Requirements:
echo   - Conda or Mamba must be installed
echo   - Internet connection for downloading packages
echo.
echo ================================================================================
echo.

REM Check if mamba is available
where mamba >nul 2>nul
if %errorlevel% == 0 (
    echo Found Mamba! Using mamba for faster installation...
    set CONDA_CMD=mamba
) else (
    where conda >nul 2>nul
    if %errorlevel% == 0 (
        echo Found Conda! Using conda...
        set CONDA_CMD=conda
    ) else (
        echo ERROR: Neither mamba nor conda found!
        echo Please install Miniforge or Anaconda first.
        echo Download Miniforge from: https://github.com/conda-forge/miniforge
        pause
        exit /b 1
    )
)

echo.
echo Creating environment 'octa-converter'...
echo.

%CONDA_CMD% env create -f environment.yml

if %errorlevel% == 0 (
    echo.
    echo ================================================================================
    echo SUCCESS! Environment created successfully.
    echo ================================================================================
    echo.
    echo To use the converter:
    echo   1. Activate environment: %CONDA_CMD% activate octa-converter
    echo   2. Run converter: python Zeiss_OCTA_Converter.py [FolderName]
    echo   Or simply double-click: 转换OCTA数据.bat
    echo.
    echo To update the environment later:
    echo   %CONDA_CMD% env update -f environment.yml
    echo.
    echo ================================================================================
) else (
    echo.
    echo ERROR: Failed to create environment!
    echo Please check your internet connection and try again.
    echo.
)

pause
