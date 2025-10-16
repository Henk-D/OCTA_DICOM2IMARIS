# -*- coding: utf-8 -*-
"""
Process ONLY the first DICOM file (the one with visible vessels)
This will create a clean 3D volume without the discontinuity
"""

import pydicom
import numpy as np
from pathlib import Path
import warnings
import json
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

warnings.filterwarnings('ignore')

def main():
    print("\n" + "="*80)
    print("SINGLE FILE OCTA Processor - Clean vessel visualization")
    print("Using ONLY the file with visible vessels")
    print("="*80 + "\n")
    
    # Data folder
    data_folder = Path(__file__).parent / "DataFiles" / "E361"
    
    # Scan DICOM files
    dcm_files = sorted(data_folder.glob("*.DCM"))
    dcm_files = [f for f in dcm_files if f.name != "DICOMDIR"]
    print(f"Found {len(dcm_files)} DICOM files\n")
    
    # Read and check metadata
    print("Checking DICOM metadata...\n")
    all_data = []
    
    for i, file_path in enumerate(dcm_files, 1):
        try:
            dcm = pydicom.dcmread(str(file_path), force=True)
            
            if not hasattr(dcm, 'PixelData'):
                continue
            
            # Fix format
            if hasattr(dcm, 'PhotometricInterpretation'):
                photo = str(dcm.PhotometricInterpretation)
                if 'MONOCHROME2' in photo:
                    dcm.PhotometricInterpretation = 'MONOCHROME2'
            
            image = dcm.pixel_array
            
            # Get metadata
            series_desc = getattr(dcm, 'SeriesDescription', 'Unknown')
            laterality = getattr(dcm, 'Laterality', 'Unknown')
            image_type = getattr(dcm, 'ImageType', 'Unknown')
            
            print(f"File [{i}]: {file_path.name}")
            print(f"  Shape: {image.shape}")
            print(f"  Series: {series_desc}")
            print(f"  Laterality: {laterality}")
            print(f"  Image Type: {image_type}")
            print(f"  Mean intensity: {image.mean():.2f}")
            print()
            
            all_data.append((image, dcm, file_path.name))
            
        except Exception as e:
            pass
    
    # Filter for shape (245, 245, 1024)
    target_shape = (245, 245, 1024)
    matching_files = [(img, dcm, name) for img, dcm, name in all_data if img.shape == target_shape]
    
    print(f"\n" + "="*80)
    print(f"Found {len(matching_files)} files with shape {target_shape}")
    print("="*80 + "\n")
    
    if len(matching_files) == 0:
        print("ERROR: No valid files!")
        return False
    
    # Analyze each file
    print("Analyzing vessel signal in each file:\n")
    for i, (img, dcm, name) in enumerate(matching_files):
        # Convert to uint8
        if img.dtype == np.int8:
            img_uint8 = img.astype(np.int16) + 128
            img_uint8 = img_uint8.astype(np.uint8)
        else:
            img_uint8 = img.astype(np.uint8)
        
        # Create MIP along depth to check vessel visibility
        mip_z = np.max(img_uint8, axis=2)
        vessel_signal = np.sum(mip_z > 180)  # Count bright pixels (vessels)
        
        print(f"File {i+1}: {name}")
        print(f"  Mean: {img.mean():.2f}, Std: {img.std():.2f}")
        print(f"  Vessel pixels (>180): {vessel_signal} ({100*vessel_signal/mip_z.size:.2f}%)")
        print()
    
    # Select the file with most vessel signal
    vessel_scores = []
    for img, dcm, name in matching_files:
        if img.dtype == np.int8:
            img_uint8 = img.astype(np.int16) + 128
            img_uint8 = img_uint8.astype(np.uint8)
        else:
            img_uint8 = img.astype(np.uint8)
        mip_z = np.max(img_uint8, axis=2)
        score = np.sum(mip_z > 180)
        vessel_scores.append(score)
    
    best_idx = np.argmax(vessel_scores)
    selected_img, selected_dcm, selected_name = matching_files[best_idx]
    
    print(f"="*80)
    print(f"SELECTED: File {best_idx+1} ({selected_name})")
    print(f"  Has the most vessel signal")
    print("="*80 + "\n")
    
    # Process the selected file
    volume_3d = selected_img
    
    print(f"3D Volume from single file:")
    print(f"  Shape: {volume_3d.shape} (Y, X, Z)")
    print(f"  Dtype: {volume_3d.dtype}")
    print(f"  Range: [{volume_3d.min()}, {volume_3d.max()}]")
    
    # Convert to uint8
    if volume_3d.dtype == np.int8:
        volume_uint8 = volume_3d.astype(np.int16) + 128
        volume_uint8 = volume_uint8.astype(np.uint8)
    else:
        vol_normalized = volume_3d.astype(np.float32)
        vol_normalized = (vol_normalized - vol_normalized.min()) / (vol_normalized.max() - vol_normalized.min())
        volume_uint8 = (vol_normalized * 255).astype(np.uint8)
    
    print(f"  Converted: uint8, range [0, 255]")
    
    # Voxel size
    scan_width_mm = 3.0
    scan_depth_mm = 2.0
    
    voxel_y = (scan_width_mm / volume_3d.shape[0]) * 1000
    voxel_x = (scan_width_mm / volume_3d.shape[1]) * 1000
    voxel_z = (scan_depth_mm / volume_3d.shape[2]) * 1000
    
    print(f"\nVoxel size:")
    print(f"  X: {voxel_x:.3f} um")
    print(f"  Y: {voxel_y:.3f} um")
    print(f"  Z: {voxel_z:.3f} um")
    
    # Save files
    print(f"\n" + "="*80)
    print("Saving Files")
    print("="*80 + "\n")
    
    output_folder = Path(__file__).parent
    
    # 1. NumPy
    npy_path = output_folder / "OCTA_SingleFile.npy"
    np.save(npy_path, volume_uint8)
    print(f"[1] NumPy: {npy_path.name} ({npy_path.stat().st_size / 1024 / 1024:.2f} MB)")
    
    # 2. Metadata
    meta_data = {
        'source_file': selected_name,
        'shape': list(volume_3d.shape),
        'shape_description': 'Y (B-scans), X (width), Z (depth)',
        'dtype': 'uint8',
        'voxel_size_um': {'X': float(voxel_x), 'Y': float(voxel_y), 'Z': float(voxel_z)},
        'patient_id': str(getattr(selected_dcm, 'PatientID', 'Unknown')),
        'study_date': str(getattr(selected_dcm, 'StudyDate', 'Unknown'))
    }
    
    json_path = output_folder / "OCTA_SingleFile_metadata.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, indent=2)
    print(f"[2] Metadata: {json_path.name}")
    
    # 3. TIFF
    try:
        import tifffile
        
        tiff_path = output_folder / "OCTA_SingleFile.tif"
        
        # Transpose to (Z, Y, X) for ImageJ
        volume_zyx = np.transpose(volume_uint8, (2, 0, 1))
        
        print(f"     Transposed shape: {volume_zyx.shape} (Z, Y, X)")
        
        resolution_x = 1.0 / (voxel_x / 1000)
        resolution_y = 1.0 / (voxel_y / 1000)
        spacing_z = voxel_z / 1000
        
        tifffile.imwrite(
            tiff_path,
            volume_zyx,
            imagej=True,
            resolution=(resolution_y, resolution_x),
            metadata={'spacing': spacing_z, 'unit': 'mm', 'axes': 'ZYX'}
        )
        
        file_size = tiff_path.stat().st_size / 1024 / 1024
        print(f"[3] TIFF: {tiff_path.name} ({file_size:.2f} MB)")
        
        if file_size > 20:
            print(f"     ✓ File size correct!")
        
    except Exception as e:
        print(f"[3] TIFF: ERROR - {e}")
    
    # 4. Preview
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        print(f"\n[4] Creating preview...")
        
        mip_z = np.max(volume_uint8, axis=2)
        mip_y = np.max(volume_uint8, axis=0)
        mip_x = np.max(volume_uint8, axis=1)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        
        axes[0, 0].imshow(mip_z, cmap='hot')
        axes[0, 0].set_title('En Face (MIP along Z) - Should show vessels!', fontsize=12, weight='bold')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(mip_y, cmap='hot', aspect='auto')
        axes[0, 1].set_title('Side view (MIP along Y)', fontsize=10)
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(mip_x, cmap='hot', aspect='auto')
        axes[1, 0].set_title('Side view (MIP along X)', fontsize=10)
        axes[1, 0].axis('off')
        
        # Central slice
        central_z = volume_uint8.shape[2] // 2
        axes[1, 1].imshow(volume_uint8[:, :, central_z], cmap='gray')
        axes[1, 1].set_title(f'Central depth slice (Z={central_z})', fontsize=10)
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        preview_path = output_folder / "OCTA_SingleFile_Preview.png"
        plt.savefig(preview_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"     Preview: {preview_path.name}")
        
    except Exception as e:
        print(f"[4] Preview: ERROR - {e}")
    
    print(f"\n" + "="*80)
    print("SUCCESS!")
    print("="*80)
    print(f"\nThis version uses ONLY ONE file - no discontinuity!")
    print(f"\nFor Imaris:")
    print(f"  File: OCTA_SingleFile.tif")
    print(f"  Voxel size: X={voxel_x:.3f}, Y={voxel_y:.3f}, Z={voxel_z:.3f} um")
    print(f"\nShould show clean, continuous vessel structure!")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("Press Enter to exit...")
            input()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        input()
