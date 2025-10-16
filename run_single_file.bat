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

python OCTA_DICOM2IMARIS_SingleFile.py

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Generated files:
echo   - OCTA_SingleFile.tif (58 MB) - Use this in Imaris!
echo   - OCTA_SingleFile_Preview.png - Check vessels here
echo.
echo Voxel size for Imaris:
echo   X: 12.245 um
echo   Y: 12.245 um
echo   Z: 1.953 um
echo.
echo This should show clean, continuous vessels!
echo No left-right separation!
echo.
pause
