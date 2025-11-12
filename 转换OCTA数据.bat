@echo off
REM Zeiss OCTA DICOM转TIFF转换器 - 快速启动脚本
REM 使用方法：将此文件拖到桌面，双击运行

echo ================================================================================
echo Zeiss Cirrus OCTA DICOM 转 TIFF 转换器
echo ================================================================================
echo.

REM 获取用户输入
set /p folder_name="请输入数据文件夹名称 (例如: HenkE433): "

if "%folder_name%"=="" (
    echo 错误：未输入文件夹名称！
    pause
    exit /b 1
)

echo.
echo 开始转换 %folder_name% ...
echo.

REM 运行Python脚本
python "%~dp0Zeiss_OCTA_Converter.py" %folder_name%

echo.
echo 转换完成！
echo.
echo 输出文件：
echo   - OCTA_%folder_name%.tif (用于Imaris)
echo   - OCTA_%folder_name%.npy (NumPy数组)
echo   - OCTA_%folder_name%_metadata.json (元数据)
echo   - OCTA_%folder_name%_Preview.png (预览图)
echo.
pause
