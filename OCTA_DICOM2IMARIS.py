# -*- coding: utf-8 -*-
"""
Universal OCTA DICOM Processor for any patient
Usage: python OCTA_processor_UNIVERSAL.py [patient_id]
Example: python OCTA_processor_UNIVERSAL.py E999

This script can process any OCTA patient data without modifying the code.
"""
import sys
import pydicom
import numpy as np
import json
from pathlib import Path
import warnings

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

warnings.filterwarnings('ignore')

def process_octa(patient_id=None):
    """Process OCTA data for a specific patient"""
    
    print("\n" + "="*80)
    print("Universal OCTA DICOM Processor")
    print("="*80 + "\n")
    
    # Determine data folder
    base_folder = Path(__file__).parent / "DataFiles"
    
    if patient_id:
        data_folder = base_folder / patient_id
    else:
        # Auto-detect: use first subfolder in DataFiles
        subfolders = [f for f in base_folder.iterdir() if f.is_dir()]
        if not subfolders:
            print("ERROR: No patient folders found in DataFiles/")
            print(f"Please create a folder like: {base_folder}/E999/")
            return False
        data_folder = subfolders[0]
        patient_id = data_folder.name
    
    if not data_folder.exists():
        print(f"ERROR: Folder not found: {data_folder}")
        print(f"Please create the folder and put DICOM files inside")
        return False
    
    print(f"Processing patient: {patient_id}")
    print(f"Data folder: {data_folder}\n")
    
    # Scan DICOM files
    dcm_files = sorted(data_folder.glob("*.DCM"))
    dcm_files = [f for f in dcm_files if f.name != "DICOMDIR"]
    
    if len(dcm_files) == 0:
        print(f"ERROR: No DICOM files found in {data_folder}")
        print("Please check the folder contains .DCM files")
        return False
    
    print(f"Found {len(dcm_files)} DICOM files\n")
    
    # Read DICOM files
    all_data = []
    for i, file_path in enumerate(dcm_files, 1):
        try:
            dcm = pydicom.dcmread(str(file_path), force=True)
            
            if not hasattr(dcm, 'PixelData'):
                print(f"  [{i:2d}] SKIP - No pixel data")
                continue
            
            # Fix format
            if hasattr(dcm, 'PhotometricInterpretation'):
                photo = str(dcm.PhotometricInterpretation)
                if 'MONOCHROME2' in photo:
                    dcm.PhotometricInterpretation = 'MONOCHROME2'
            
            image = dcm.pixel_array
            print(f"  [{i:2d}] OK - Shape: {image.shape}, Mean: {image.mean():.2f}")
            all_data.append((image, dcm))
            
        except Exception as e:
            print(f"  [{i:2d}] ERROR - {str(e)[:50]}")
    
    if len(all_data) == 0:
        print("\nERROR: No valid data found!")
        return False
    
    print(f"\nSuccessfully read {len(all_data)} files\n")
    
    # Find 3D shape (typical OCTA: 245x245x1024 or similar)
    target_shape_3d = None
    for img, _ in all_data:
        if len(img.shape) == 3 and img.shape[0] > 100 and img.shape[2] > 500:
            target_shape_3d = img.shape
            break
    
    if not target_shape_3d:
        print("ERROR: No suitable 3D data found!")
        print("Expected shape like (245, 245, 1024)")
        return False
    
    # Filter candidates
    candidates = [(img, dcm) for img, dcm in all_data if img.shape == target_shape_3d]
    print(f"Found {len(candidates)} files with shape {target_shape_3d}\n")
    
    # Select file with most vessel signal
    best_score = 0
    best_data = None
    
    for img, dcm in candidates:
        # Convert to uint8
        if img.dtype == np.int8:
            img_uint8 = img.astype(np.int16) + 128
            img_uint8 = img_uint8.astype(np.uint8)
        else:
            img_norm = (img - img.min()) / (img.max() - img.min())
            img_uint8 = (img_norm * 255).astype(np.uint8)
        
        # Score by vessel signal (bright pixels in MIP)
        mip = np.max(img_uint8, axis=2)
        score = np.sum(mip > 180)
        
        if score > best_score:
            best_score = score
            best_data = (img, dcm, img_uint8)
    
    if not best_data:
        print("ERROR: No suitable data found!")
        return False
    
    volume_raw, selected_dcm, volume_uint8 = best_data
    
    print(f"Selected best file:")
    print(f"  Vessel signal score: {best_score}")
    print(f"  Volume shape: {volume_uint8.shape} (Y, X, Z)")
    print(f"  Data type: uint8")
    print(f"  Range: [0, 255]\n")
    
    # Calculate voxel size (typical OCTA parameters)
    scan_width_mm = 3.0
    scan_depth_mm = 2.0
    
    voxel_y = (scan_width_mm / volume_uint8.shape[0]) * 1000
    voxel_x = (scan_width_mm / volume_uint8.shape[1]) * 1000
    voxel_z = (scan_depth_mm / volume_uint8.shape[2]) * 1000
    
    print(f"Voxel size (for Imaris):")
    print(f"  X: {voxel_x:.3f} um")
    print(f"  Y: {voxel_y:.3f} um")
    print(f"  Z: {voxel_z:.3f} um\n")
    
    # Save files
    output_folder = Path(__file__).parent
    base_name = f"OCTA_{patient_id}"
    
    print("="*80)
    print("Saving Files")
    print("="*80 + "\n")
    
    # 1. NumPy
    npy_path = output_folder / f"{base_name}.npy"
    np.save(npy_path, volume_uint8)
    print(f"[1] NumPy: {npy_path.name} ({npy_path.stat().st_size / 1024 / 1024:.2f} MB)")
    
    # 2. Metadata
    metadata = {
        'patient_id': patient_id,
        'shape': list(volume_uint8.shape),
        'shape_description': 'Y (B-scans), X (width), Z (depth)',
        'dtype': 'uint8',
        'voxel_size_um': {
            'X': float(voxel_x),
            'Y': float(voxel_y),
            'Z': float(voxel_z)
        },
        'study_date': str(getattr(selected_dcm, 'StudyDate', 'Unknown')),
        'scan_parameters': {
            'scan_width_mm': scan_width_mm,
            'scan_depth_mm': scan_depth_mm
        }
    }
    
    json_path = output_folder / f"{base_name}_metadata.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"[2] Metadata: {json_path.name}")
    
    # 3. TIFF
    try:
        import tifffile
        
        # Transpose to (Z, Y, X) for ImageJ
        volume_zyx = np.transpose(volume_uint8, (2, 0, 1))
        print(f"     Transposed shape: {volume_zyx.shape} (Z, Y, X)")
        
        tiff_path = output_folder / f"{base_name}.tif"
        
        resolution_x = 1.0 / (voxel_x / 1000)
        resolution_y = 1.0 / (voxel_y / 1000)
        spacing_z = voxel_z / 1000
        
        tifffile.imwrite(
            tiff_path,
            volume_zyx,
            imagej=True,
            resolution=(resolution_y, resolution_x),
            metadata={
                'spacing': spacing_z,
                'unit': 'mm',
                'axes': 'ZYX'
            }
        )
        
        file_size = tiff_path.stat().st_size / 1024 / 1024
        print(f"[3] TIFF: {tiff_path.name} ({file_size:.2f} MB)")
        
        if file_size > 20:
            print(f"     ✓ File size correct!")
        else:
            print(f"     ⚠ File size seems small")
    
    except ImportError:
        print(f"[3] TIFF: SKIPPED (install: pip install tifffile)")
    except Exception as e:
        print(f"[3] TIFF: ERROR - {str(e)[:100]}")
    
    # 4. Preview
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        print(f"\n[4] Creating preview...")
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        
        # En face view (MIP along Z)
        mip_z = np.max(volume_uint8, axis=2)
        axes[0, 0].imshow(mip_z, cmap='hot')
        axes[0, 0].set_title(f'Patient {patient_id} - En Face View\nCheck for vessel network!', 
                            fontsize=12, weight='bold')
        axes[0, 0].axis('off')
        
        # Side view Y
        mip_y = np.max(volume_uint8, axis=0)
        axes[0, 1].imshow(mip_y, cmap='hot', aspect='auto')
        axes[0, 1].set_title('Side view (MIP along Y)', fontsize=10)
        axes[0, 1].axis('off')
        
        # Side view X
        mip_x = np.max(volume_uint8, axis=1)
        axes[1, 0].imshow(mip_x, cmap='hot', aspect='auto')
        axes[1, 0].set_title('Side view (MIP along X)', fontsize=10)
        axes[1, 0].axis('off')
        
        # Central slice
        central_z = volume_uint8.shape[2] // 2
        axes[1, 1].imshow(volume_uint8[:, :, central_z], cmap='gray')
        axes[1, 1].set_title(f'Central depth slice (Z={central_z}/{volume_uint8.shape[2]})', 
                            fontsize=10)
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        preview_path = output_folder / f"{base_name}_Preview.png"
        plt.savefig(preview_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"     Preview: {preview_path.name}")
        print(f"     ✓ Check En Face view (top-left) for vessels!")
    
    except Exception as e:
        print(f"[4] Preview: ERROR - {str(e)[:50]}")
    
    # Final summary
    print(f"\n" + "="*80)
    print("PROCESSING COMPLETE!")
    print("="*80)
    print(f"\nPatient: {patient_id}")
    print(f"Output files: {base_name}.*")
    print(f"\nFor Imaris:")
    print(f"  1. Open: {base_name}.tif")
    print(f"  2. Set voxel size:")
    print(f"     X = {voxel_x:.3f} um")
    print(f"     Y = {voxel_y:.3f} um")
    print(f"     Z = {voxel_z:.3f} um")
    print(f"  3. Use Volume Rendering or MIP")
    print(f"  4. Threshold: 180-255 for vessel signal")
    print(f"\nVerification:")
    print(f"  - Check {base_name}_Preview.png for vessels")
    print(f"  - File size should be ~60 MB")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    # Get patient ID from command line or auto-detect
    patient_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    if patient_id:
        print(f"\nProcessing specified patient: {patient_id}")
    else:
        print(f"\nNo patient ID specified, will auto-detect from DataFiles/")
    
    try:
        success = process_octa(patient_id)
        if not success:
            print("\nProcessing failed! Check error messages above.")
        else:
            print("Success! Files are ready for Imaris.")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\nUser interrupted")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
