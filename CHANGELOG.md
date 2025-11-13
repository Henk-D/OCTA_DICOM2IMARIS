# Changelog

All notable changes to OCTA_DICOM2IMARIS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-16

### 🎉 Initial Release

First stable release of OCTA_DICOM2IMARIS - a tool to convert Carl Zeiss CIRRUS OCTA DICOM files to Imaris-compatible TIFF format.

### Added
- **Core Processing Script** (`OCTA_DICOM2IMARIS.py`)
  - Universal processor accepting patient ID as command-line argument
  - Auto-detection of patient folders in `DataFiles/`
  - Automatic vessel signal scoring to select best DICOM file
  - Proper data transposition from (Y,X,Z) to (Z,Y,X) for Imaris
  - int8 to uint8 conversion for proper intensity display
  
- **Single File Processor** (`OCTA_DICOM2IMARIS_SingleFile.py`)
  - Specialized processor for patient E361
  - Avoids left-right separation issue from merging multiple files
  
- **Windows Batch Launchers**
  - `run_universal.bat` - One-click launcher for universal processor
  - `run_single_file.bat` - One-click launcher for single file processor
  - UTF-8 encoding support for Chinese characters
  
- **Output Files**
  - 3D TIFF volumes in (Z,Y,X) format
  - 4-panel preview images (XY, XZ, YZ projections + 3D MIP)
  - JSON metadata files with voxel sizes and patient info
  - NumPy arrays (.npy) for Python post-processing
  
- **Documentation**
  - Complete Chinese guide (`README.md`)
  - English documentation (`README_EN.md`)
  - Quick start guide (`快速上手.md`)
  - Imaris visualization guide (`血管可视化指南.md`)
  - Technical problem analysis (`左右分离问题解决方案.md`)
  - Project overview (`开始阅读我.md`)
  
- **Development Tools**
  - `requirements.txt` - Python dependencies
  - `.gitignore` - Git ignore rules for data files
  - `LICENSE` - MIT License
  
- **Quality Assurance**
  - Automatic vessel signal validation
  - Preview generation for visual quality check
  - Detailed error messages and logging
  - Diagnostic visualization of data structure

### Technical Details
- Supports Carl Zeiss CIRRUS OCTA DICOM format
- Default data shape: (245, 245, 1024) → transposes to (1024, 245, 245)
- Voxel sizes: X=12.245 μm, Y=12.245 μm, Z=1.953 μm (typical)
- Vessel detection threshold: intensity > 180 in MIP
- Output TIFF size: ~50-100 MB per patient

### Known Issues
- **Left-right separation**: When multiple DICOM files with different intensity distributions are merged, Imaris may show discontinuity. **Solution**: Use single file processor.
- **Windows encoding**: Some Chinese characters may display incorrectly in PowerShell. **Solution**: Script automatically sets UTF-8 encoding.

---

## [2.0.0] - 2025-11-12

### 🎉 Major Update - GUI, NIfTI Export, and Environment Management

### Added
- **GUI Interface** (`OCTA_Converter_GUI.py`)
  - Complete graphical user interface with tkinter
  - Visual folder selection with dropdown menu
  - Real-time conversion log display
  - Progress bar animation
  - Auto-open output folder on completion
  - Launch script: `启动GUI.bat`

- **NIfTI Format Export**
  - Medical imaging standard format (`.nii.gz`)
  - Compatible with ITK-SNAP, 3D Slicer, FSL, SPM
  - Embedded voxel sizes in NIfTI header
  - Compressed format (~38MB per volume)
  - Added `nibabel>=3.2.0` dependency

- **Conda/Mamba Environment Support**
  - `environment.yml` configuration file
  - `setup_environment.bat` automated setup script
  - Environment name: `octa-converter`
  - Supports both mamba and conda package managers

- **Extended Resolution Support**
  - 8x8mm scans (640x640 pixels)
  - 9x9mm scans (730x730 pixels)
  - 12x12mm scans (980x980 pixels)
  - Automatic estimation for custom resolutions

- **New Documentation**
  - `快速开始.md` - Quick start guide
  - Updated all docs with NIfTI format information
  - Multi-resolution support tables

### Changed
- **Fixed Batch Script Encoding**
  - Added `chcp 65001` to all `.bat` files
  - Switched to English interface to avoid encoding issues
  - `转换OCTA数据.bat` updated with NIfTI information
  
- **Updated Legacy Scripts**
  - `run_universal.bat` now calls `Zeiss_OCTA_Converter.py`
  - `run_single_file.bat` now calls `Zeiss_OCTA_Converter.py`
  - Added interactive folder name input

- **Enhanced Output**
  - Now generates **5 files** per conversion:
    1. `.tif` - Imaris (59MB)
    2. `.nii.gz` - Medical imaging software (38MB)
    3. `.npy` - NumPy array (59MB)
    4. `.json` - Metadata (1KB)
    5. `.png` - MIP preview (2MB)

### Technical Details
- NIfTI uses RAS+ coordinate system
- Voxel sizes in mm (embedded in header)
- GUI runs conversion in separate thread (non-blocking)
- Environment setup script auto-detects mamba/conda

### Fixed
- Chinese character display issues in Windows batch files
- Batch script compatibility with new main script name

---

## [Unreleased]

### Planned Features
- [ ] Batch processing multiple folders
- [ ] Support for other OCTA device manufacturers
- [ ] Automatic Imaris project file (.ims) generation
- [ ] Advanced vessel enhancement filters
- [ ] Docker container for cross-platform compatibility
- [ ] Integration with cloud storage (Google Drive, OneDrive)

### Under Consideration
- [ ] DICOM tag editor
- [ ] Vessel segmentation tools
- [ ] Statistical analysis of vessel density
- [ ] Web-based viewer

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

---

## Contributing

See [CONTRIBUTING.md] for how to contribute to this changelog.

---

**Last Updated**: 2025-10-16  
**Maintainer**: Henk Shang
