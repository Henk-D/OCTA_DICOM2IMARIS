# Zeiss OCTA DICOM 转换器

将Zeiss Cirrus HD-OCT OCTA DICOM文件转换为Imaris可读的TIFF格式。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行转换

**方法A：命令行**
```bash
python Zeiss_OCTA_Converter.py HenkE433
```

**方法B：双击运行**
- Windows: 双击 `转换OCTA数据.bat`
- 输入文件夹名称

### 3. 在Imaris中打开

1. 打开生成的 `OCTA_<文件夹>.tif`
2. 体素大小已自动设置
3. 调整对比度即可

## 输出文件

所有输出文件保存在 `Results/<文件夹名>/` 目录下：

- `OCTA_<文件夹>.tif` - TIFF文件（Imaris用）
- `OCTA_<文件夹>.npy` - NumPy数组
- `OCTA_<文件夹>_metadata.json` - 扫描参数
- `OCTA_<文件夹>_Preview.png` - 预览图

例如：`Results/HenkE433/OCTA_HenkE433.tif`

## 功能特性

✅ 自动修复Zeiss DICOM元数据损坏  
✅ 支持JPEG 2000解压缩  
✅ 自动检测维度错误并修正  
✅ 适应不同扫描分辨率（3x3mm, 6x6mm等）  
✅ 自动选择最佳质量体积  

## 支持的数据

- 245x245x1024 (3x3mm)
- 490x490x1024 (6x6mm)
- 其他Zeiss Cirrus OCTA分辨率

## 详细文档

查看 [使用说明.md](使用说明.md) 了解更多细节。

## 常见问题

**Q: 看不到血管？**  
A: 调整Imaris的对比度，或检查是否选择了正确的数据文件。

**Q: 某些文件无法读取？**  
A: 正常现象。脚本会自动跳过损坏的文件，选择最佳的可用数据。

**Q: 体素大小不对？**  
A: 检查 `metadata.json` 中的扫描参数，必要时手动调整。

## 技术支持

- 查看预览图判断转换质量
- 检查metadata.json了解数据参数
- 损坏的DICOM文件会被自动跳过

---

**UCSF OCTA 数据分析** | 2025
