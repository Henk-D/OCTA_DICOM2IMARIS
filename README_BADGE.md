# OCTA_DICOM2IMARIS

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/status-ready_for_release-brightgreen)

**Convert Carl Zeiss CIRRUS OCTA DICOM files to Imaris-compatible TIFF format with proper 3D structure.**

[中文文档](README.md) | [English Documentation](README_EN.md) | [Quick Start](快速上手.md) | [Release Guide](GITHUB_RELEASE_GUIDE.md)

---

## 🎯 What is OCTA_DICOM2IMARIS?

A Python tool to convert Optical Coherence Tomography Angiography (OCTA) DICOM files from Carl Zeiss CIRRUS devices into 3D TIFF volumes for visualization in Bitplane Imaris.

### ✨ Key Features

- ✅ Universal processing - works with any patient data
- ✅ Automatic file selection based on vessel signals
- ✅ Proper 3D structure (Z,Y,X) for Imaris
- ✅ Metadata preservation and quality verification
- ✅ Batch processing support
- ✅ Windows-optimized with UTF-8 encoding

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare data
# Place DICOM files in: DataFiles/PATIENT_ID/

# 3. Run processor
python OCTA_DICOM2IMARIS.py PATIENT_ID

# 4. Open in Imaris
# File: OCTA_PATIENT_ID.tif
# Voxel sizes from: OCTA_PATIENT_ID_metadata.json
```

**Windows Users:** Double-click `run_universal.bat`

---

## 📖 Documentation

### For Users
- 🇨🇳 **中文**: [README.md](README.md) | [快速上手](快速上手.md) | [开始阅读我](开始阅读我.md)
- 🇬🇧 **English**: [README_EN.md](README_EN.md)

### For Developers
- 🛠️ [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- 📝 [CHANGELOG.md](CHANGELOG.md) - Version history

### For Publishers
- 🚀 [GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md) - How to release on GitHub
- 📊 [PROJECT_RENAME_SUMMARY.md](PROJECT_RENAME_SUMMARY.md) - Renaming summary

### Technical Guides
- 🔬 [血管可视化指南.md](血管可视化指南.md) - Imaris visualization guide
- 🔧 [左右分离问题解决方案.md](左右分离问题解决方案.md) - Technical analysis
- 📋 [文件清理总结.md](文件清理总结.md) - File cleanup summary

---

## 📊 Project Status

### ✅ Completed Features

- [x] Universal processor for any patient
- [x] Single-file processor (avoids merge artifacts)
- [x] Windows batch launchers
- [x] Comprehensive documentation (Chinese + English)
- [x] Quality assurance (preview generation)
- [x] Metadata export (JSON)

### 🔄 Upcoming Features

- [ ] GUI interface
- [ ] Cross-platform support (Linux, Mac)
- [ ] Support for other OCTA devices
- [ ] Docker container
- [ ] Automated testing

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Carl Zeiss Meditec for CIRRUS OCTA platform
- Bitplane (Oxford Instruments) for Imaris software
- Python community for scientific libraries

---

## 📧 Contact

- **GitHub Issues**: Report bugs or request features
- **Documentation**: See README.md / README_EN.md for full details

---

## 🌟 Citation

If you use this tool in your research, please cite:

```bibtex
@software{octa_dicom2imaris,
  title = {OCTA_DICOM2IMARIS: Convert OCTA DICOM to Imaris TIFF},
  author = {Henk Shang},
  year = {2025},
  version = {1.0.0},
  url = {https://github.com/HenkShang/OCTA_DICOM2IMARIS}
}
```

---

**Made with ❤️ by Henk Shang | Advancing OCTA Research**

**Last Updated:** 2025-10-16 | **Version:** 1.0.0 | **Status:** Ready for Release 🚀
