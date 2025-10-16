# Contributing to OCTA_DICOM2IMARIS

Thank you for your interest in contributing to OCTA_DICOM2IMARIS! 🎉

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Title**: Brief description of the problem
2. **Environment**: 
   - OS (Windows/Linux/Mac)
   - Python version
   - Package versions (`pip list`)
3. **Steps to reproduce**:
   - What commands did you run?
   - What data were you using?
4. **Expected vs Actual behavior**
5. **Error messages**: Full error log if available
6. **Screenshots**: If applicable

### Suggesting Features

We welcome feature suggestions! Please:

1. Check existing issues to avoid duplicates
2. Clearly describe the feature and use case
3. Explain why it would be useful
4. Consider implementation complexity

### Code Contributions

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/HenkShang/OCTA_DICOM2IMARIS.git
cd OCTA_DICOM2IMARIS
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# Or for bug fixes:
git checkout -b fix/bug-description
```

#### 3. Make Changes

- Follow existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

#### 4. Test

```bash
# Run the script with test data
python OCTA_DICOM2IMARIS.py TEST_PATIENT

# Verify output
# - Check TIFF file opens in Imaris
# - Verify vessels are visible
# - Ensure metadata is correct
```

#### 5. Commit

```bash
git add .
git commit -m "Add feature: brief description"

# Use conventional commits format:
# feat: Add new feature
# fix: Fix bug
# docs: Update documentation
# style: Code style changes
# refactor: Code refactoring
# test: Add tests
```

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
# Then create a Pull Request on GitHub
```

## 📝 Code Style

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use meaningful variable names
- Add docstrings for functions
- Keep functions short and focused

```python
def process_dicom(file_path, threshold=180):
    """
    Process a single DICOM file.
    
    Args:
        file_path (Path): Path to DICOM file
        threshold (int): Intensity threshold for vessel detection
        
    Returns:
        np.ndarray: Processed 3D volume
    """
    # Implementation
```

### Comments

- Use `#` for inline comments
- Use docstrings for functions/classes
- Explain "why", not "what"

```python
# Good
# Select file with highest vessel score to avoid merge artifacts
best_file = max(files, key=lambda f: calculate_score(f))

# Avoid
# Get the best file
best_file = max(files, key=lambda f: calculate_score(f))
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Script runs without errors
- [ ] Output TIFF file size is reasonable (50-100 MB)
- [ ] Preview image shows vessels
- [ ] Metadata JSON contains correct voxel sizes
- [ ] TIFF opens correctly in Imaris
- [ ] Vessels are visible in Imaris Volume rendering

### Test Data

Use the example patient in `DataFiles/EXAMPLE_PATIENT/` for testing.

## 📚 Documentation

### Update Documentation When:

- Adding new features → Update `README.md` and `README_EN.md`
- Fixing bugs → Update `CHANGELOG.md`
- Changing CLI → Update usage examples
- Adding dependencies → Update `requirements.txt`

### Documentation Style

- Use clear, simple language
- Provide code examples
- Add screenshots for visual features
- Support both English and Chinese

## 🎯 Priority Areas

We especially welcome contributions in:

1. **Cross-platform support** (Linux, Mac)
2. **GUI interface** (PyQt, Tkinter)
3. **Support for other OCTA devices** (Optovue, Topcon, etc.)
4. **Automated testing** (pytest, unittest)
5. **Performance optimization**
6. **Docker containerization**

## ⚠️ Important Notes

### Patient Data Privacy

- **NEVER commit real patient data**
- Always use de-identified data for examples
- Check `.gitignore` before committing

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow GitHub community guidelines

## 🔄 Review Process

1. **Automated checks**: Code will be checked for style and errors
2. **Manual review**: Maintainers will review your code
3. **Testing**: Changes will be tested with example data
4. **Feedback**: You may be asked to make changes
5. **Merge**: Once approved, your PR will be merged!

## 📧 Questions?

- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and ideas
- **Email**: [henk.shang@example.com] for private inquiries

## 🙏 Recognition

All contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to better OCTA research tools! 🔬🚀

---

**Last Updated**: 2025-10-16  
**Maintainer**: Henk Shang
