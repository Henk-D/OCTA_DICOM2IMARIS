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

## [Unreleased]

### Planned Features
- [ ] GUI interface for easier operation
- [ ] Batch processing with progress bar
- [ ] Support for other OCTA device manufacturers
- [ ] Automatic Imaris project file (.ims) generation
- [ ] Advanced vessel enhancement filters
- [ ] Multi-language support (English UI)
- [ ] Docker container for cross-platform compatibility
- [ ] Integration with cloud storage (Google Drive, OneDrive)

### Under Consideration
- [ ] DICOM tag editor
- [ ] Vessel segmentation tools
- [ ] Statistical analysis of vessel density
- [ ] Export to other formats (HDF5, NIfTI)
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
