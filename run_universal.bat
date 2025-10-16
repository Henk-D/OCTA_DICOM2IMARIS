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
    echo No patient ID specified, auto-detecting...
    python OCTA_DICOM2IMARIS.py
) else (
    echo Processing patient: %1
    python OCTA_DICOM2IMARIS.py %1
)

echo.
echo ========================================
echo.
pause
