# OCTA_DICOM2IMARIS

Convert Carl Zeiss CIRRUS OCTA DICOM files to Imaris-compatible TIFF format with proper 3D structure and metadata.

[中文文档](README.md) | **English Documentation**

---

## 🎯 Overview

**OCTA_DICOM2IMARIS** is a Python tool designed to convert Optical Coherence Tomography Angiography (OCTA) DICOM files from Carl Zeiss CIRRUS devices into 3D TIFF volumes suitable for visualization in Bitplane Imaris.

### Key Features

- ✅ **Universal Processing**: Works with any patient data without code modification
- ✅ **Automatic File Selection**: Intelligently selects DICOM files with vessel signals
- ✅ **Proper 3D Structure**: Correctly transposes data to (Z, Y, X) for Imaris
- ✅ **Metadata Preservation**: Exports voxel sizes and patient information
- ✅ **Preview Generation**: Creates en face projections for quality verification
- ✅ **Batch Processing**: Process multiple patients in sequence
- ✅ **Windows-Optimized**: UTF-8 encoding and batch launchers included

---

## 📋 Requirements

### System Requirements
- Windows 10/11 (PowerShell support)
- Python 3.8+
- 2GB+ RAM
- Sufficient disk space (output TIFF ~50-100 MB per patient)

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Core packages:**
- `pydicom >= 2.3.0` - DICOM file reading
- `numpy >= 1.20.0` - Array processing
- `tifffile >= 2021.0.0` - TIFF export
- `matplotlib >= 3.3.0` - Preview generation

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/HenkShang/OCTA_DICOM2IMARIS.git
cd OCTA_DICOM2IMARIS

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data

Place your DICOM files in the following structure:
```
DataFiles/
├── PATIENT_001/
│   ├── file1.DCM
│   ├── file2.DCM
│   └── ...
├── PATIENT_002/
│   └── ...
```

### 3. Run Processing

**Option A: Windows Batch Launcher (Easiest)**
```bash
# Double-click run_universal.bat
# Or run from command line:
run_universal.bat PATIENT_001
```

**Option B: Python Script**
```bash
# Process specific patient
python OCTA_DICOM2IMARIS.py PATIENT_001

# Auto-detect first patient in DataFiles/
python OCTA_DICOM2IMARIS.py
```

### 4. Verify Output

Check the generated files:
- `OCTA_PATIENT_001.tif` - Import this into Imaris
- `OCTA_PATIENT_001_Preview.png` - Verify vessels are visible
- `OCTA_PATIENT_001_metadata.json` - Contains voxel sizes

### 5. Open in Imaris

1. Open Imaris (version 9.0+)
2. File → Open → Select `OCTA_PATIENT_001.tif`
3. Set voxel sizes from metadata.json:
   - X: 12.245 μm
   - Y: 12.245 μm
   - Z: 1.953 μm (adjust based on your data)
4. Create Volume rendering to visualize vessels

---

## 📖 Detailed Usage

### Command-Line Interface

```bash
# Basic usage
python OCTA_DICOM2IMARIS.py [PATIENT_ID]

# Examples
python OCTA_DICOM2IMARIS.py E361      # Process patient E361
python OCTA_DICOM2IMARIS.py           # Auto-detect patient
```

### Batch Processing

Process multiple patients:

```bash
# Method 1: Sequential commands
python OCTA_DICOM2IMARIS.py PATIENT_001
python OCTA_DICOM2IMARIS.py PATIENT_002
python OCTA_DICOM2IMARIS.py PATIENT_003

# Method 2: Loop (PowerShell)
foreach ($p in 'PATIENT_001','PATIENT_002','PATIENT_003') {
    python OCTA_DICOM2IMARIS.py $p
}

# Method 3: Loop (Bash/Git Bash)
for p in PATIENT_001 PATIENT_002 PATIENT_003; do
    python OCTA_DICOM2IMARIS.py $p
done
```

### Output Files

For each patient, the following files are generated:

| File | Description | Size |
|------|-------------|------|
| `OCTA_[ID].tif` | 3D TIFF volume for Imaris | ~50-100 MB |
| `OCTA_[ID]_Preview.png` | 4-panel quality check (XY, XZ, YZ, 3D MIP) | ~500 KB |
| `OCTA_[ID]_metadata.json` | Voxel sizes, shape, patient info | ~1 KB |
| `OCTA_[ID].npy` | Raw NumPy array for Python processing | ~60 MB |

---

## 🔧 Advanced Configuration

### Vessel Signal Detection

The script automatically scores DICOM files by counting high-intensity pixels (>180) in Maximum Intensity Projection (MIP). The file with the highest score is selected.

To adjust the threshold, edit `OCTA_DICOM2IMARIS.py`:

```python
def calculate_vessel_score(data):
    mip = np.max(data, axis=2)
    score = np.sum(mip > 180)  # Change 180 to desired threshold
    return score
```

### Data Type Conversion

DICOM data is converted from int8 to uint8:

```python
# Default conversion
data_uint8 = data.astype(np.int8).astype(np.uint8)

# Alternative: Normalize to full range
data_uint8 = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)
```

---

## 📊 Data Structure

### DICOM Input

Carl Zeiss CIRRUS OCTA files typically have:
- Shape: `(Y, X, Z)` = `(245, 245, 1024)`
- Y: B-scan positions
- X: A-scan width
- Z: Depth layers (1024 axial scans)

### TIFF Output

The script transposes data to Imaris-compatible format:
- Shape: `(Z, Y, X)` = `(1024, 245, 245)`
- Z: Depth (stack slices)
- Y: Height
- X: Width

---

## 🐛 Troubleshooting

### Issue: "No DICOM files found"

**Cause**: No `.DCM` files in `DataFiles/[PATIENT_ID]/`

**Solution**:
```bash
# Check folder structure
ls DataFiles/PATIENT_001/

# Ensure files have .DCM extension
# Rename if needed: ren *.EX.DCM *.DCM
```

### Issue: "No vessels visible in Preview.png"

**Cause**: Original DICOM data may lack vessel signal

**Solutions**:
1. Check original data quality in DICOM viewer
2. Adjust intensity threshold (see Advanced Configuration)
3. Try different DICOM files from the same acquisition

### Issue: "Left-right separation in Imaris"

**Cause**: Multiple DICOM files were incorrectly merged

**Solution**: Use `OCTA_DICOM2IMARIS_SingleFile.py` to process only one file:
```bash
python OCTA_DICOM2IMARIS_SingleFile.py
```

### Issue: "Unicode errors on Windows"

**Cause**: PowerShell default encoding (GBK) conflicts with UTF-8

**Solution**: Script automatically sets UTF-8 encoding. If errors persist:
```powershell
# Run in PowerShell
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
python OCTA_DICOM2IMARIS.py PATIENT_001
```

---

## 🔬 Technical Background

### Why This Tool?

**Problem 1**: OCTA DICOM files from Carl Zeiss devices use unusual data ordering that Imaris doesn't recognize.

**Problem 2**: Multiple DICOM files from the same scan may have different intensity distributions, causing visualization artifacts when merged.

**Solution**: This tool:
1. Automatically detects and selects files with vessel signals
2. Correctly transposes data to `(Z, Y, X)` format
3. Preserves voxel spacing for accurate 3D reconstruction
4. Generates preview images for quality assurance

### Data Processing Pipeline

```
DICOM Files (245×245×1024)
    ↓
Load with pydicom (force=True)
    ↓
Score by vessel signal (MIP > 180)
    ↓
Select best file
    ↓
Convert int8 → uint8
    ↓
Transpose to (Z, Y, X)
    ↓
Export TIFF + metadata
    ↓
Generate preview (4 panels)
```

---

## 📚 Documentation Structure

- **README_EN.md** (this file) - English documentation
- **README.md** - Chinese documentation (中文完整指南)
- **快速上手.md** - Quick start guide (Chinese)
- **血管可视化指南.md** - Imaris visualization guide (Chinese)
- **左右分离问题解决方案.md** - Technical analysis (Chinese)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Citation

If you use this tool in your research, please cite:

```bibtex
@software{octa_dicom2imaris,
  title = {OCTA_DICOM2IMARIS: Convert OCTA DICOM to Imaris TIFF},
  author = {Henk Shang},
  year = {2025},
  url = {https://github.com/HenkShang/OCTA_DICOM2IMARIS}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Carl Zeiss Meditec for CIRRUS OCTA platform
- Bitplane (Oxford Instruments) for Imaris software
- Python community for excellent scientific libraries

---

## 📧 Contact

For questions, issues, or suggestions:

- **GitHub Issues**: [Report a bug](https://github.com/HenkShang/OCTA_DICOM2IMARIS/issues)
- **Email**: henk.shang@example.com

---

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version**: 1.0.0 (October 2025)

---

## ⚠️ Disclaimer

This tool is provided for research purposes only. Always verify output quality before using data for clinical decisions or publications.

---

**Made with ❤️ by Henk Shang | Advancing OCTA Research**
