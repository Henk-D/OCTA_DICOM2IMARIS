# 🚀 如何将 OCTA_DICOM2IMARIS 发布到 GitHub

这份指南将帮助您将项目发布到 GitHub 并进行后续管理。

## 📋 准备清单

### ✅ 已完成的准备工作

- [x] 重命名核心脚本为 `OCTA_DICOM2IMARIS.py`
- [x] 创建 LICENSE 文件（MIT License）
- [x] 创建 .gitignore 文件
- [x] 创建英文文档 README_EN.md
- [x] 创建 CHANGELOG.md
- [x] 创建 CONTRIBUTING.md
- [x] 更新所有文档中的脚本引用
- [x] 创建 DataFiles/README.md

### ⚠️ 发布前需要做的事

- [ ] **重要：删除或移动真实患者数据**
- [ ] 检查所有文件是否包含敏感信息
- [ ] 更新 README.md 中的联系方式
- [ ] 更新 CHANGELOG.md 中的日期
- [ ] 创建 GitHub 仓库

---

## 🔒 第一步：保护患者隐私

### 1. 移动真实数据到 .gitignore

```powershell
# 当前数据文件（E361）不应上传到 GitHub
# 已在 .gitignore 中配置，但请确认：

# 检查 .gitignore 是否包含：
# DataFiles/*/
# OCTA_*.tif
# OCTA_*.npy
# OCTA_*.ims
```

### 2. 创建示例数据（可选）

```powershell
# 如果要提供示例数据，请使用完全去标识化的数据
# 或者创建一个模拟数据集
mkdir DataFiles/EXAMPLE_PATIENT
# 添加去标识化的示例 DICOM 文件
```

---

## 🌐 第二步：创建 GitHub 仓库

### 方法 A：通过 GitHub 网站（推荐）

1. **登录 GitHub**: https://github.com
2. **创建新仓库**:
   - 点击右上角 "+" → "New repository"
   - Repository name: `OCTA_DICOM2IMARIS`
   - Description: `Convert Carl Zeiss CIRRUS OCTA DICOM to Imaris TIFF`
   - 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize with README"（我们已经有了）
   - **不要**添加 .gitignore（我们已经有了）
   - **不要**选择 License（我们已经有了）
3. **点击 "Create repository"**

### 方法 B：通过 Git 命令行

```bash
# 在 GitHub 网站创建空仓库后，在本地执行：
cd "d:\Henk Shang-Henk3(DataProcessing)\DataProcessing\Method_Project\0_RawData\OCTA\ROSE\DICOM\data\DICOM Files Test"
git init
git add .
git commit -m "Initial commit: OCTA_DICOM2IMARIS v1.0.0"
git branch -M main
git remote add origin https://github.com/HenkShang/OCTA_DICOM2IMARIS.git
git push -u origin main
```

---

## 📦 第三步：初始化 Git 仓库

### 1. 初始化并添加文件

```powershell
# 进入项目目录
cd "d:\Henk Shang-Henk3(DataProcessing)\DataProcessing\Method_Project\0_RawData\OCTA\ROSE\DICOM\data\DICOM Files Test"

# 初始化 Git
git init

# 查看将要添加的文件
git status

# 添加所有文件（.gitignore 会自动排除数据文件）
git add .

# 查看暂存的文件
git status

# 提交
git commit -m "Initial commit: OCTA_DICOM2IMARIS v1.0.0

- Add core processing scripts (OCTA_DICOM2IMARIS.py)
- Add English and Chinese documentation
- Add Windows batch launchers
- Add requirements.txt, LICENSE, .gitignore
- Add CHANGELOG.md and CONTRIBUTING.md"
```

### 2. 关联远程仓库

```powershell
# 替换为你的 GitHub 用户名
git remote add origin https://github.com/HenkShang/OCTA_DICOM2IMARIS.git

# 查看远程仓库
git remote -v
```

### 3. 推送到 GitHub

```powershell
# 首次推送
git push -u origin main

# 如果遇到错误（远程有 README 等文件），使用：
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 🏷️ 第四步：创建发布版本（Release）

### 在 GitHub 网站操作：

1. 进入你的仓库页面
2. 点击右侧 "Releases" → "Create a new release"
3. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: 复制 CHANGELOG.md 中的内容
4. 点击 "Publish release"

### 或使用命令行：

```powershell
# 创建标签
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"

# 推送标签
git push origin v1.0.0
```

---

## 📝 第五步：完善仓库信息

### 1. 添加 Topics（主题标签）

在 GitHub 仓库页面，点击右侧 "About" 旁边的齿轮图标，添加：

- `octa`
- `dicom`
- `imaris`
- `medical-imaging`
- `python`
- `zeiss-cirrus`
- `3d-visualization`
- `biomedical-research`

### 2. 更新 Description

```
Convert Carl Zeiss CIRRUS OCTA DICOM to Imaris TIFF | 转换 OCTA DICOM 为 Imaris 格式
```

### 3. 添加 Website（可选）

如果有相关论文或实验室网站，添加链接。

---

## 📄 第六步：更新联系方式和链接

### 需要更新的文件：

1. **README_EN.md** (第 287 行):
   ```markdown
   - **GitHub Issues**: [Report a bug](https://github.com/HenkShang/OCTA_DICOM2IMARIS/issues)
   - **Email**: henk.shang@example.com
   ```
   → 改为你的真实 GitHub 用户名和邮箱

2. **README_EN.md** (第 296 行):
   ```bibtex
   url = {https://github.com/HenkShang/OCTA_DICOM2IMARIS}
   ```

3. **CONTRIBUTING.md** (第 177 行):
   ```markdown
   - **Email**: [henk.shang@example.com]
   ```

### 批量替换命令：

```powershell
# 替换 HenkShang 为你的 GitHub 用户名
$username = "你的GitHub用户名"
$email = "你的邮箱"

Get-ChildItem -Filter *.md -Recurse | ForEach-Object {
    (Get-Content $_.FullName -Raw -Encoding UTF8) `
        -replace 'HenkShang', $username `
        -replace 'your\.email@institution\.edu', $email |
    Set-Content $_.FullName -Encoding UTF8 -NoNewline
}
```

---

## 🎨 第七步：添加 README Badge（徽章）

在 README.md 和 README_EN.md 的开头添加：

```markdown
# OCTA_DICOM2IMARIS

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

Convert Carl Zeiss CIRRUS OCTA DICOM files to Imaris-compatible TIFF format.
```

---

## 📊 第八步：项目结构优化（可选）

### 推荐的目录结构：

```
OCTA_DICOM2IMARIS/
├── .github/
│   └── workflows/          # GitHub Actions（未来可添加）
├── docs/                   # 文档目录
│   ├── zh/                 # 中文文档
│   │   ├── 快速上手.md
│   │   ├── 血管可视化指南.md
│   │   └── 左右分离问题解决方案.md
│   └── images/             # 图片
│       └── DIAGNOSTIC_DataStructure.png
├── DataFiles/
│   ├── README.md
│   └── EXAMPLE_PATIENT/    # 示例数据（可选）
├── examples/               # 示例脚本（可选）
├── OCTA_DICOM2IMARIS.py    # 主脚本
├── OCTA_DICOM2IMARIS_SingleFile.py
├── run_universal.bat
├── run_single_file.bat
├── requirements.txt
├── README.md               # 中文主文档
├── README_EN.md            # 英文文档
├── LICENSE
├── .gitignore
├── CHANGELOG.md
└── CONTRIBUTING.md
```

### 移动文件（可选）：

```powershell
# 创建 docs 目录
mkdir docs\zh
mkdir docs\images

# 移动中文文档
Move-Item "快速上手.md" "docs\zh\"
Move-Item "血管可视化指南.md" "docs\zh\"
Move-Item "左右分离问题解决方案.md" "docs\zh\"
Move-Item "文件清理总结.md" "docs\zh\"
Move-Item "问题解决总结.md" "docs\zh\"
Move-Item "开始阅读我.md" "docs\zh\"

# 移动图片
Move-Item "DIAGNOSTIC_DataStructure.png" "docs\images\"

# 更新文档中的链接引用...
```

---

## 🔄 第九步：后续维护

### 日常更新流程：

```powershell
# 1. 修改代码或文档后
git status

# 2. 添加更改
git add .

# 3. 提交
git commit -m "描述你的更改"

# 4. 推送到 GitHub
git push
```

### 发布新版本：

```powershell
# 1. 更新 CHANGELOG.md
# 2. 提交更改
git add CHANGELOG.md
git commit -m "Release v1.1.0"

# 3. 创建标签
git tag -a v1.1.0 -m "Version 1.1.0"

# 4. 推送
git push
git push origin v1.1.0

# 5. 在 GitHub 创建 Release
```

---

## 📣 第十步：推广项目

### 1. 添加到相关社区

- **Python 医学影像**: Reddit r/computational_imaging
- **生物医学图像分析**: Research Gate, ResearchGate
- **OCTA 研究**: 相关学术会议和研讨会

### 2. 撰写博客文章

介绍工具的开发背景和使用方法。

### 3. 在论文中引用

如果用于研究，在 Methods 部分引用：

```
OCTA data was converted using OCTA_DICOM2IMARIS 
(https://github.com/HenkShang/OCTA_DICOM2IMARIS, v1.0.0).
```

### 4. 收集反馈

- 鼓励用户提交 Issues
- 响应 Pull Requests
- 根据反馈改进功能

---

## ⚠️ 重要提醒

### 患者数据隐私：

1. **绝对不要**上传真实患者数据
2. 定期检查 `.git` 历史中是否有敏感信息
3. 如果不小心上传了敏感数据：
   ```powershell
   # 从 Git 历史中完全删除文件
   git filter-branch --force --index-filter `
     "git rm --cached --ignore-unmatch DataFiles/E361/*" `
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```

### 版权和许可：

- MIT License 允许他人自由使用、修改、分发
- 如果使用第三方代码，确保遵守其许可协议
- 在 README 中感谢贡献者

---

## 📧 需要帮助？

如果在发布过程中遇到问题：

1. **Git 问题**: [GitHub Docs](https://docs.github.com/)
2. **隐私问题**: 咨询您的机构伦理审查委员会
3. **技术问题**: GitHub Issues 或联系维护者

---

## ✅ 发布清单总结

- [ ] 删除/移动真实患者数据
- [ ] 检查敏感信息
- [ ] 创建 GitHub 仓库
- [ ] 初始化 Git 并推送
- [ ] 创建 v1.0.0 Release
- [ ] 添加 Topics 和 Description
- [ ] 更新联系方式
- [ ] 添加 README Badge
- [ ] （可选）优化项目结构
- [ ] 推广项目

---

**祝您发布顺利！🎉🚀**

如果这个项目帮助了其他研究者，别忘了在 GitHub 添加 ⭐ Star！

---

**文档版本**: 1.0  
**最后更新**: 2025-10-16  
**作者**: Henk Shang
