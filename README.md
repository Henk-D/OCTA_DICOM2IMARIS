# 📖 OCTA数据处理指南

## ⚡ 快速开始 - 当前数据已处理完成

### 在Imaris中打开当前数据

**文件：** `OCTA_SingleFile.tif` (58.78 MB)

**体素尺寸：**
```
X: 12.245 微米
Y: 12.245 微米  
Z: 1.953 微米
```

**验证：** 打开 `OCTA_SingleFile_Preview.png` 查看左上角应该有血管网络

---

## 🆕 处理新患者数据

### 方法1：修改现有脚本（适合偶尔处理）

1. **准备数据**
   ```
   将新患者的DICOM文件放入：
   DataFiles/E999/  (E999改成你的患者ID)
   ```

2. **修改脚本**
   - 打开 `OCTA_DICOM2IMARIS_SingleFile.py`
   - 找到第26行左右：
   ```python
   data_folder = Path(__file__).parent / "DataFiles" / "E361"
   ```
   - 改为：
   ```python
   data_folder = Path(__file__).parent / "DataFiles" / "E999"  # 你的患者ID
   ```

3. **运行**
   ```
   双击: run_single_file.bat
   ```

---

### 方法2：使用通用脚本（推荐，适合批量处理）

1. **创建通用脚本**
   - 将下方的 `OCTA_DICOM2IMARIS.py` 代码保存为新文件

2. **运行方式**
   ```bash
   # 处理指定患者
   python OCTA_DICOM2IMARIS.py E999
   
   # 自动处理DataFiles/下第一个患者
   python OCTA_DICOM2IMARIS.py
   ```

3. **批量处理**
   ```bash
   python OCTA_DICOM2IMARIS.py E361
   python OCTA_DICOM2IMARIS.py E999
   python OCTA_DICOM2IMARIS.py E1000
   ```

---

## 📋 输出文件说明

处理完成后会生成4个文件：

| 文件 | 用途 | 大小 |
|------|------|------|
| `OCTA_[PatientID].tif` | Imaris打开这个 | ~60 MB |
| `OCTA_[PatientID]_Preview.png` | 验证有血管 | 几MB |
| `OCTA_[PatientID].npy` | Python处理 | ~60 MB |
| `OCTA_[PatientID]_metadata.json` | 参数信息 | 几KB |

---

## 🔧 通用处理脚本代码

保存以下代码为 `OCTA_DICOM2IMARIS.py`:

```python
# -*- coding: utf-8 -*-
"""
Universal OCTA DICOM Processor for any patient
Usage: python OCTA_DICOM2IMARIS.py [patient_id]
"""
import sys, pydicom, numpy as np, json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def process_octa(patient_id=None):
    print("\n" + "="*80)
    print("Universal OCTA Processor")
    print("="*80 + "\n")
    
    base_folder = Path(__file__).parent / "DataFiles"
    
    if patient_id:
        data_folder = base_folder / patient_id
    else:
        subfolders = [f for f in base_folder.iterdir() if f.is_dir()]
        if not subfolders:
            print("ERROR: No folders in DataFiles/")
            return False
        data_folder = subfolders[0]
        patient_id = data_folder.name
    
    if not data_folder.exists():
        print(f"ERROR: {data_folder} not found")
        return False
    
    print(f"Patient: {patient_id}")
    print(f"Folder: {data_folder}\n")
    
    dcm_files = sorted([f for f in data_folder.glob("*.DCM") if f.name != "DICOMDIR"])
    if not dcm_files:
        print("ERROR: No DCM files!")
        return False
    
    print(f"Found {len(dcm_files)} files\n")
    
    # Read files
    all_data = []
    for i, fp in enumerate(dcm_files, 1):
        try:
            dcm = pydicom.dcmread(str(fp), force=True)
            if not hasattr(dcm, 'PixelData'):
                continue
            if hasattr(dcm, 'PhotometricInterpretation'):
                if 'MONOCHROME2' in str(dcm.PhotometricInterpretation):
                    dcm.PhotometricInterpretation = 'MONOCHROME2'
            img = dcm.pixel_array
            print(f"  [{i}] {img.shape}, mean={img.mean():.1f}")
            all_data.append((img, dcm))
        except Exception as e:
            print(f"  [{i}] ERROR")
    
    if not all_data:
        print("\nNo valid data!")
        return False
    
    # Find 3D shape
    target = None
    for img, _ in all_data:
        if len(img.shape) == 3 and img.shape[0] > 100 and img.shape[2] > 500:
            target = img.shape
            break
    
    if not target:
        print("No 3D data found!")
        return False
    
    candidates = [(img, dcm) for img, dcm in all_data if img.shape == target]
    print(f"\n{len(candidates)} files with shape {target}\n")
    
    # Select best (most vessel signal)
    best_score, best_data = 0, None
    for img, dcm in candidates:
        img_u8 = (img.astype(np.int16) + 128).astype(np.uint8) if img.dtype == np.int8 else ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)
        score = np.sum(np.max(img_u8, axis=2) > 180)
        if score > best_score:
            best_score, best_data = score, (img, dcm, img_u8)
    
    if not best_data:
        print("No suitable data!")
        return False
    
    _, sel_dcm, vol = best_data
    print(f"Selected file: vessel_score={best_score}")
    print(f"Volume: {vol.shape} (Y,X,Z)\n")
    
    # Voxel size
    vx = vy = (3.0 / vol.shape[0]) * 1000
    vz = (2.0 / vol.shape[2]) * 1000
    print(f"Voxel: X={vx:.3f}, Y={vy:.3f}, Z={vz:.3f} um\n")
    
    # Save
    out = Path(__file__).parent
    name = f"OCTA_{patient_id}"
    
    print("="*80)
    print("Saving...")
    print("="*80 + "\n")
    
    # NPY
    npy_p = out / f"{name}.npy"
    np.save(npy_p, vol)
    print(f"[1] {npy_p.name} ({npy_p.stat().st_size/1024/1024:.1f}MB)")
    
    # JSON
    meta = {'patient': patient_id, 'shape': list(vol.shape), 
            'voxel_um': {'X': vx, 'Y': vy, 'Z': vz}}
    with open(out / f"{name}_metadata.json", 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"[2] {name}_metadata.json")
    
    # TIFF
    try:
        import tifffile
        vol_zyx = np.transpose(vol, (2,0,1))
        tif_p = out / f"{name}.tif"
        tifffile.imwrite(tif_p, vol_zyx, imagej=True,
                        resolution=(1000/vy, 1000/vx),
                        metadata={'spacing': vz/1000, 'unit': 'mm', 'axes': 'ZYX'})
        print(f"[3] {tif_p.name} ({tif_p.stat().st_size/1024/1024:.1f}MB)")
    except: print("[3] TIFF error")
    
    # Preview
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(2,2, figsize=(12,12))
        ax[0,0].imshow(np.max(vol, axis=2), cmap='hot')
        ax[0,0].set_title(f'{patient_id} - En Face (check vessels!)', weight='bold')
        ax[0,0].axis('off')
        
        ax[0,1].imshow(np.max(vol, axis=0), cmap='hot', aspect='auto')
        ax[0,1].set_title('Side Y'); ax[0,1].axis('off')
        
        ax[1,0].imshow(np.max(vol, axis=1), cmap='hot', aspect='auto')
        ax[1,0].set_title('Side X'); ax[1,0].axis('off')
        
        ax[1,1].imshow(vol[:,:,vol.shape[2]//2], cmap='gray')
        ax[1,1].set_title('Central slice'); ax[1,1].axis('off')
        
        plt.tight_layout()
        prev_p = out / f"{name}_Preview.png"
        plt.savefig(prev_p, dpi=150)
        plt.close()
        print(f"[4] {prev_p.name}")
    except: print("[4] Preview error")
    
    print(f"\n" + "="*80)
    print("SUCCESS!")
    print("="*80)
    print(f"\nImaris: {name}.tif")
    print(f"Voxel: X={vx:.3f}, Y={vy:.3f}, Z={vz:.3f} um")
    print("="*80 + "\n")
    return True

if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        if not process_octa(pid):
            print("Failed!")
        input("Press Enter...")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        input()
```

---

## 📊 文件结构

```
工作文件夹/
├── OCTA_DICOM2IMARIS_SingleFile.py    ← 当前E361专用
├── OCTA_DICOM2IMARIS.py    ← 通用脚本（需创建）
├── run_single_file.bat             ← 一键运行
│
├── DataFiles/
│   ├── E361/                       ← 当前患者DICOM
│   └── E999/                       ← 新患者放这里
│
├── OCTA_SingleFile.tif             ← 当前患者输出
├── OCTA_SingleFile_Preview.png
├── OCTA_SingleFile.npy
└── OCTA_SingleFile_metadata.json
```

---

## 🆘 常见问题

### Q: Preview图没有血管？
**A:** 脚本会自动选择血管信号最强的文件。如果所有文件都没有血管，检查原始DICOM数据。

### Q: Imaris中还是左右分离？
**A:** 使用 `OCTA_DICOM2IMARIS_SingleFile.py` 或 `OCTA_DICOM2IMARIS.py`，不要合并多个文件。

### Q: 体素尺寸不确定？
**A:** 默认使用 3mm×3mm扫描区域，2mm深度。如需修改，编辑脚本中的 `scan_width_mm` 和 `scan_depth_mm`。

### Q: 如何批量处理？
**A:** 使用通用脚本循环处理：
```bash
python OCTA_DICOM2IMARIS.py E361
python OCTA_DICOM2IMARIS.py E999
python OCTA_DICOM2IMARIS.py E1000
```

---

## 📚 详细文档

- `血管可视化指南.md` - Imaris详细使用说明
- `左右分离问题解决方案.md` - 技术分析
- `问题解决总结.md` - 问题诊断历史

---

## ✅ 处理新数据检查清单

- [ ] DICOM文件放入 `DataFiles/[PatientID]/`
- [ ] 修改脚本患者ID 或 使用通用脚本
- [ ] 运行脚本
- [ ] 检查生成4个文件（.tif, .png, .npy, .json）
- [ ] 打开Preview确认有血管
- [ ] 在Imaris中测试打开
- [ ] 设置体素尺寸（见metadata.json）

---

**更新日期：** 2025年10月16日  
**适用数据：** Carl Zeiss CIRRUS OCTA DICOM
