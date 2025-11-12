# -*- coding: utf-8 -*-
"""
使用oct-converter库测试读取Zeiss Cirrus OCTA DICOM文件
"""

import sys
import warnings
warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from oct_converter.readers import Dicom
    print("✓ oct-converter 已安装\n")
except ImportError as e:
    print(f"✗ oct-converter 未安装: {e}")
    print("请运行: pip install oct-converter")
    sys.exit(1)

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def test_oct_converter_reader(folder_name):
    """使用oct-converter测试读取DICOM文件"""
    
    print("="*80)
    print(f"测试文件夹: {folder_name}")
    print("="*80)
    
    folder = Path(__file__).parent / "DataFiles" / folder_name
    if not folder.exists():
        print(f"错误: 文件夹不存在: {folder}")
        return None
    
    dicom_files = sorted([f for f in folder.glob('*.DCM') if f.name != 'DICOMDIR'])
    print(f"找到 {len(dicom_files)} 个DICOM文件\n")
    
    successful_reads = []
    
    for i, file_path in enumerate(dicom_files, 1):
        print(f"文件 [{i}/{len(dicom_files)}]: {file_path.name[:40]}...")
        
        try:
            # 尝试使用oct-converter读取
            reader = Dicom(str(file_path))
            volume = reader.read_oct_volume()
            
            if volume is not None:
                print(f"  ✓ 成功读取!")
                print(f"    Shape: {volume.shape}")
                print(f"    Dtype: {volume.dtype}")
                print(f"    Range: [{volume.min()}, {volume.max()}]")
                print(f"    Mean: {volume.mean():.2f}, Std: {volume.std():.2f}")
                
                successful_reads.append({
                    'file_num': i,
                    'file_name': file_path.name,
                    'volume': volume,
                    'shape': volume.shape,
                    'mean': volume.mean(),
                    'std': volume.std()
                })
            else:
                print(f"  ✗ 返回None")
                
        except Exception as e:
            error_msg = str(e)[:80]
            print(f"  ✗ 错误: {error_msg}")
        
        print()
    
    print(f"成功读取: {len(successful_reads)}/{len(dicom_files)} 个文件\n")
    
    return successful_reads

# 测试不同数据集
print("开始测试 oct-converter 库\n")

datasets = ['E361', 'HenkE433', 'HenkE434', 'HenkE435', 'HenkE436']
results = {}

for dataset in datasets:
    result = test_oct_converter_reader(dataset)
    if result:
        results[dataset] = result
        print(f"{'='*80}\n")

# 总结
print("="*80)
print("测试总结")
print("="*80)

if results:
    for dataset, data in results.items():
        print(f"\n{dataset}:")
        print(f"  成功读取: {len(data)} 个文件")
        if data:
            shapes = set([tuple(d['shape']) for d in data])
            print(f"  形状: {shapes}")
            best = max(data, key=lambda x: x['std'])
            print(f"  最佳文件 (最高对比度): File {best['file_num']}")
            print(f"    Shape: {best['shape']}, Mean: {best['mean']:.1f}, Std: {best['std']:.1f}")
else:
    print("\n未能成功读取任何文件")
    print("\noct-converter可能不支持这种Zeiss DICOM格式")
    print("将尝试其他方法...")

print("\n按Enter键退出...")
input()
