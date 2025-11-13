@echo off
chcp 65001 >nul
REM Zeiss OCTA DICOM Converter - Quick Launch Script
REM Usage: Double-click to run

echo ================================================================================
echo Zeiss Cirrus OCTA DICOM to TIFF/NIfTI Converter
echo ================================================================================
echo.

REM Get user input
set /p folder_name="Enter data folder name (e.g., HenkE433): "

if "%folder_name%"=="" (
    echo ERROR: No folder name provided!
    pause
    exit /b 1
)

echo.
echo Converting %folder_name% ...
echo.

REM Run Python script
python "%~dp0Zeiss_OCTA_Converter.py" %folder_name%

echo.
echo Conversion complete!
echo.
echo Output files in Results\%folder_name%\:
echo   - OCTA_%folder_name%.tif (for Imaris)
echo   - OCTA_%folder_name%.nii.gz (for medical imaging software)
echo   - OCTA_%folder_name%.npy (NumPy array)
echo   - OCTA_%folder_name%_metadata.json (metadata)
echo   - OCTA_%folder_name%_Preview.png (preview)
echo.
pause
