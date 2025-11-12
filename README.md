# Zeiss Cirrus OCTA DICOM转换工具

## 功能
将Zeiss Cirrus HD-OCT导出的OCTA DICOM文件转换为Imaris可用的TIFF格式。

## 特点
- ✅ 自动修复损坏的DICOM元数据
- ✅ 处理JPEG 2000压缩
- ✅ 自动检测并修复维度错误
- ✅ 智能选择最佳血管造影图文件
- ✅ 适应不同分辨率（245×245×1024和490×490×1024）
- ✅ 生成预览图和元数据

## 文件结构
```
OCTA_DICOM2IMARIS/
├── DataFiles/          # 放置DICOM源文件
│   ├── E361/
│   ├── HenkE433/
│   └── ...
├── Results/            # 输出结果
│   ├── E361/
│   │   ├── E361.tif           # Imaris使用
│   │   ├── E361.npy           # NumPy格式
│   │   ├── E361_metadata.json # 元数据
│   │   └── E361_Preview.png   # 预览图
│   └── ...
└── Zeiss_OCTA_Converter.py  # 转换脚本
```

## 使用方法

### 1. 准备数据
将Zeiss导出的DICOM文件放入 `DataFiles/<文件夹名>/` 目录

### 2. 运行转换
```powershell
cd OCTA_DICOM2IMARIS
python Zeiss_OCTA_Converter.py <文件夹名>
```

例如：
```powershell
python Zeiss_OCTA_Converter.py HenkE433
```

### 3. 批量处理
```powershell
foreach ($dataset in @('HenkE433', 'HenkE434', 'HenkE435', 'HenkE436')) {
    python Zeiss_OCTA_Converter.py $dataset
}
```

## 输出文件说明

### 1. TIFF文件 (.tif)
- 用于Imaris导入
- 格式：ZYX（深度×高度×宽度）
- 包含正确的体素尺寸元数据

### 2. NumPy文件 (.npy)
- Python NumPy格式
- 可用于进一步分析

### 3. 元数据文件 (_metadata.json)
- 包含：
  - 源文件信息
  - 图像尺寸
  - 体素大小
  - 血管分析结果
  - 患者信息

### 4. 预览图 (_Preview.png)
- 4个视图：
  - En Face (MIP沿Z轴)
  - 侧视图 (MIP沿Y轴)
  - 侧视图 (MIP沿X轴)
  - 中央切片

## Imaris导入设置

1. 打开Imaris
2. File → Open → 选择 `.tif` 文件
3. 体素大小已自动设置：
   - 245×245: X=12.245 µm, Y=12.245 µm, Z=1.953 µm
   - 490×490: X=12.245 µm, Y=12.245 µm, Z=1.953 µm

## 已知问题和解决方案

### 问题1：看不到血管信号
**原因**：DICOM文件可能包含多种类型的数据（结构图、血管造影图等）

**解决**：脚本会自动选择最可能是血管造影图的文件（基于vessel score）

### 问题2：3个结构堆叠
**原因**：维度混淆或选择了错误的文件类型

**解决**：脚本已自动检测并修正维度问题

### 问题3：部分文件无法读取
**状态**：正常现象

**说明**：每个数据集通常包含8个文件，其中：
- 2-3个可以成功解压和读取
- 其余文件可能损坏或格式不同
- 脚本会自动选择最佳的可读文件

## 依赖包
- pydicom
- pylibjpeg
- pylibjpeg-openjpeg
- numpy
- tifffile
- matplotlib

## 安装依赖
```powershell
pip install pydicom pylibjpeg pylibjpeg-openjpeg numpy tifffile matplotlib
```

## 测试结果

### 已成功测试的数据集
- ✅ E361 (245×245×1024)
- ✅ HenkE433 (245×245×1024)
- ✅ HenkE434 (245×245×1024)
- ✅ HenkE435 (245×245×1024)
- ✅ HenkE436 (490×490×1024)

### 典型读取情况
每个数据集 (8个DICOM文件):
- 通常可读取：2-3个文件
- 其中选择最佳：1个文件
- 这是正常的，因为不是所有文件都是血管造影图

## 故障排除

### 错误："找不到数据文件夹"
确保DICOM文件在 `DataFiles/<文件夹名>/` 目录下

### 错误："无法读取任何有效文件"
检查：
1. DICOM文件是否损坏
2. 是否安装了所有依赖包
3. 是否为Zeiss Cirrus格式

### 输出全黑或全白
可能选择了错误的文件类型。查看metadata.json中的vessel_analysis部分，确认选择的文件特征。

## 联系与支持
如有问题，请检查：
1. Results文件夹中的Preview.png
2. metadata.json中的vessel_analysis
3. 控制台输出的文件分析信息

---
最后更新：2025年11月6日
