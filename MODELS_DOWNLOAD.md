# 📦 AI Models Download Guide

This guide explains how to download and install the required AI models for Cool PWA Icon Generator.

---

## 📋 Required Models

Two AI model files are required (total ~7GB):

| Model File | Size | Purpose |
|------------|------|---------|
| `LiberteRedmond.safetensors` | ~3.5GB | Base Stable Diffusion model |
| `IconsRedmond15V-Icons.safetensors` | ~3.5GB | LoRA fine-tuning for icon generation |

---

## 🔗 Download Links

### Option 1: Hugging Face (Recommended)

1. **LiberteRedmond.safetensors**
   - Visit: [https://huggingface.co/](https://huggingface.co/)
   - Search for "LiberteRedmond" or "Stable Diffusion 1.5"
   - Download the `.safetensors` file

2. **IconsRedmond15V-Icons.safetensors**
   - Visit: [https://huggingface.co/](https://huggingface.co/)
   - Search for "IconsRedmond" or "Icon LoRA"
   - Download the `.safetensors` file

### Option 2: CivitAI

1. Visit [https://civitai.com/](https://civitai.com/)
2. Search for the model names
3. Download the `.safetensors` versions (preferred over `.ckpt`)

---

## 📁 Installation

1. **Create models directory** (if it doesn't exist):
   ```
   [project_folder]/models/
   ```

2. **Place downloaded files** in the models directory:
   ```
   [project_folder]/models/
   ├── LiberteRedmond.safetensors
   └── IconsRedmond15V-Icons.safetensors
   ```

3. **Verify filenames match exactly:**
   - ✅ `LiberteRedmond.safetensors`
   - ✅ `IconsRedmond15V-Icons.safetensors`
   - ❌ DO NOT rename the files
   - ❌ Case-sensitive on Linux/macOS

---

## ✅ Verification

After placing the models, verify your installation:

### Windows
```cmd
dir models
```

### Linux/macOS
```bash
ls -lh models/
```

Expected output:
```
LiberteRedmond.safetensors              (~3.5GB)
IconsRedmond15V-Icons.safetensors       (~3.5GB)
```

---

## 🐛 Troubleshooting

### "Models not found" error

**Check file location:**
```
✅ Correct: [project_folder]/models/LiberteRedmond.safetensors
❌ Wrong:   [project_folder]/LiberteRedmond.safetensors
❌ Wrong:   [project_folder]/models/subfolder/LiberteRedmond.safetensors
```

**Check filenames:**
- Must be exact: `LiberteRedmond.safetensors` (not `liberte_redmond.safetensors`)
- Must be exact: `IconsRedmond15V-Icons.safetensors`
- Case-sensitive on Linux/macOS

**Check file format:**
- Must be `.safetensors` format
- If you downloaded `.ckpt` files, look for `.safetensors` versions instead

### Download interrupted

If downloads are interrupted or corrupted:
1. Delete the partial file
2. Re-download from the source
3. Verify file size matches expected size (~3.5GB each)

### Slow downloads

- Use a download manager for large files
- Try alternative mirrors if available
- Download during off-peak hours

---

## 🔒 Security Note

- Only download models from trusted sources (Hugging Face, CivitAI)
- Verify file sizes match expected values
- `.safetensors` format is safer than `.ckpt` (no arbitrary code execution)

---

## 💾 Storage Recommendations

- **SSD recommended** - Faster model loading
- **Keep backups** - Models are large and take time to download
- **Free space** - Ensure at least 10GB free for models + temporary files

---

## 📞 Need Help?

If you encounter issues downloading or installing models:
- Check [GitHub Issues](https://github.com/yourusername/cool-pwa-icon-generator/issues)
- Verify your internet connection for large downloads
- Ensure you have sufficient disk space

---

**After installing models, return to [README.md](README.md) to continue setup.**