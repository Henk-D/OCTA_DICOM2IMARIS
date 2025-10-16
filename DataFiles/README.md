# DataFiles Folder

This folder contains patient DICOM data organized by patient ID.

## 📁 Folder Structure

Each patient should have their own subfolder:

```
DataFiles/
├── PATIENT_001/
│   ├── file1.EX.DCM
│   ├── file2.EX.DCM
│   └── DICOMDIR (optional)
├── PATIENT_002/
│   └── ...
└── EXAMPLE_PATIENT/
    └── (example DICOM files)
```

## 📝 Naming Convention

- **Folder names**: Use patient IDs (e.g., `E361`, `PATIENT_001`, `20250620_001`)
- **DICOM files**: Any name ending with `.DCM` or `.dcm`
- **Case sensitivity**: Not required (Windows)

## ⚠️ Important Notes

### 1. Patient Privacy
- **DO NOT commit real patient data to Git**
- Add patient folders to `.gitignore` (already configured)
- Only share de-identified or example data publicly

### 2. File Organization
- One patient = One subfolder
- Put all DICOM files from one scan session in the same folder
- The script will automatically select the best file with vessel signals

### 3. Typical DICOM Names
Carl Zeiss CIRRUS OCTA files typically look like:
```
12AIT1XQS0Z2B3IK77YPBVBV9NLAFSUFE27IOLS4X2ZU.EX.DCM
27F8HZ5CNJK2B3IK77YP1MBV9NLAFSUFE27IOLS4X2ZU.EX.DCM
```

## 🚀 Quick Start

### Add New Patient Data

1. Create a new folder with patient ID:
   ```
   DataFiles/PATIENT_NEW/
   ```

2. Copy DICOM files into the folder

3. Run the processor:
   ```bash
   python OCTA_DICOM2IMARIS.py PATIENT_NEW
   ```

## 🔍 Example Data

An example dataset is included in `EXAMPLE_PATIENT/` folder:
- De-identified DICOM files
- Use this to test the pipeline
- Not real patient data

## 📊 Data Requirements

### DICOM File Properties
- **Device**: Carl Zeiss CIRRUS OCTA
- **Format**: DICOM (.DCM)
- **Typical shape**: (245, 245, 1024)
- **Modality**: Optical Coherence Tomography

### Minimum Requirements
- At least 1 DICOM file per patient
- File size: Typically 10-50 MB per file
- Valid DICOM header (script uses `force=True` for corrupted files)

## 🛠️ Troubleshooting

### "No DICOM files found"
- Check file extension is `.DCM` or `.dcm`
- Verify files are in the correct patient subfolder
- Use `dir` (Windows) or `ls` (Linux/Mac) to list files

### "No vessel signals detected"
- Original DICOM data may lack vessel information
- Try different acquisition files
- Check data quality in a DICOM viewer

### "Folder not found"
- Ensure patient folder exists in `DataFiles/`
- Check spelling of patient ID
- Use `run_universal.bat` and it will list available folders

## 📧 Need Help?

See main [README.md](../README.md) or [README_EN.md](../README_EN.md) for full documentation.

---

**Last Updated**: 2025-10-16  
**Directory**: `DataFiles/`
