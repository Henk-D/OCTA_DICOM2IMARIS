@echo off
REM OCTA_DICOM2IMARIS - Single File Processor
chcp 65001 >nul
echo ========================================
echo OCTA_DICOM2IMARIS - Single File Processor
echo ========================================
echo.
echo This version processes ONLY the file with visible vessels
echo Avoids the left-right separation issue in Imaris
echo.

echo NOTE: This script is deprecated. Use Zeiss_OCTA_Converter.py instead.
echo The new version automatically selects the best volume.
echo.
set /p folder_name="Enter data folder name: "
if "%folder_name%"=="" (
    echo ERROR: No folder name provided!
    pause
    exit /b 1
)

python Zeiss_OCTA_Converter.py %folder_name%

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Output files are in Results\%folder_name%\
echo   - OCTA_%folder_name%.tif - Use in Imaris
echo   - OCTA_%folder_name%.nii.gz - Use in ITK-SNAP/3D Slicer
echo   - OCTA_%folder_name%_Preview.png - Check vessels here
echo.
echo Voxel sizes are embedded in the files!
echo.
pause
