# 📁 Models Folder Setup - Quick Reference

## ⚠️ CRITICAL: Correct Location

The models folder **MUST** be inside the project directory:

```
✅ CORRECT:
g:\newlocalicons\models\
├── LiberteRedmond.safetensors
└── IconsRedmond15V-Icons.safetensors

❌ WRONG:
g:\models\           (Not in project directory)
d:\models\           (Wrong drive)
c:\models\           (Wrong drive)
```

## 🎯 Exact File Paths Required

```
g:\newlocalicons\models\LiberteRedmond.safetensors
g:\newlocalicons\models\IconsRedmond15V-Icons.safetensors
```

## 🔧 Setup Steps

1. **Navigate to project directory:**
   ```bash
   cd g:\newlocalicons
   ```

2. **Create models folder:**
   ```bash
   mkdir models
   ```

3. **Download model files:**
   
   **File 1: LiberteRedmond.safetensors (~2GB)**
   - Source: HuggingFace
   - Direct link: https://huggingface.co/artificialguybr/Liberte/tree/main
   - Download the `LiberteRedmond.safetensors` file from the repository
   
   **File 2: IconsRedmond15V-Icons.safetensors (~150MB)**
   - Source: CivitAI
   - Direct link: https://civitai.com/models/206191/iconsredmond-15v-app-icons-lora-for-sd-liberteredmond-sd-15
   - Click "Download" button on the page to get the `.safetensors` file

4. **Move files to models folder:**
   ```bash
   # Move the downloaded .safetensors files to:
   g:\newlocalicons\models\
   ```

5. **Verify:**
   ```bash
   dir models
   # Should show both .safetensors files
   ```

## ✅ Verification Checklist

Before starting the application, verify:

- [ ] Models folder exists at `g:\newlocalicons\models\`
- [ ] LiberteRedmond.safetensors is in the models folder
- [ ] IconsRedmond15V-Icons.safetensors is in the models folder
- [ ] File sizes are approximately correct (~2GB and ~150MB)
- [ ] Files have `.safetensors` extension (not .zip, .rar, etc.)

## 🚨 Common Mistakes

**Mistake 1: Wrong Location**
```
❌ Placed at: g:\models\
✅ Should be:  g:\newlocalicons\models\
```

**Mistake 2: Wrong Drive**
```
❌ Placed at: d:\models\
✅ Should be:  g:\newlocalicons\models\
```

**Mistake 3: Not in Project**
```
❌ Placed at: c:\users\username\models\
✅ Should be:  g:\newlocalicons\models\
```

## 🔍 How the App Finds Models

The application uses **relative paths** from the project directory:

```python
# In config.py:
BASE_DIR = Path(__file__).parent      # g:\newlocalicons
MODELS_DIR = BASE_DIR / "models"      # g:\newlocalicons\models
```

This means the models **must** be inside the project folder.

## 📞 Troubleshooting

**Error: "Model files not found"**

Solution:
```bash
# Check if files exist
dir g:\newlocalicons\models

# Should show:
# LiberteRedmond.safetensors
# IconsRedmond15V-Icons.safetensors
```

**Error: "No such file or directory"**

Solution: Create the models folder first:
```bash
cd g:\newlocalicons
mkdir models
```

## 🎓 Understanding the Path

```
g:\                          ← Drive
└── newlocalicons\          ← Project root directory
    ├── models\             ← Models folder (YOU CREATE THIS)
    │   ├── LiberteRedmond.safetensors          ← Model file 1
    │   └── IconsRedmond15V-Icons.safetensors   ← Model file 2
    ├── frontend\
    ├── main.py
    ├── config.py
    └── ...other project files
```

## ✨ Quick Start After Setup

Once models are in the correct location:

```bash
cd g:\newlocalicons
start.bat
```

The application will automatically find and load the models from `g:\newlocalicons\models\`.