@echo off
REM OCTA_DICOM2IMARIS - Universal Processor Launcher
chcp 65001 >nul
echo ========================================
echo OCTA_DICOM2IMARIS - Universal Processor
echo ========================================
echo.
echo This script can process any patient's OCTA data
echo.
echo Usage:
echo   1. Put DICOM files in DataFiles/[PatientID]/
echo   2. Run: run_universal.bat [PatientID]
echo   3. Or just run without PatientID to auto-detect
echo.
echo ========================================
echo.

if "%1"=="" (
    echo No folder name specified!
    echo Usage: run_universal.bat [FolderName]
    echo Example: run_universal.bat HenkE433
    echo.
    set /p folder_name="Enter data folder name: "
    if "!folder_name!"=="" (
        echo ERROR: No folder name provided!
        pause
        exit /b 1
    )
    python Zeiss_OCTA_Converter.py !folder_name!
) else (
    echo Processing folder: %1
    python Zeiss_OCTA_Converter.py %1
)

echo.
echo ========================================
echo.
pause
