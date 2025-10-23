# 🚀 Cool PWA Icon Generator - Complete Setup Guide
## Offline AI-Powered Progressive Web App Icon Maker

This guide will walk you through setting up the Cool PWA Icon Generator from scratch.

## 📋 Pre-Installation Checklist

Before starting, ensure you have:

- [ ] Windows 10/11 (or Linux/Mac with modifications)
- [ ] 20GB+ free disk space
- [ ] Stable internet connection for downloads
- [ ] Administrator privileges (for installations)

## 1️⃣ Install Required Software

### Python 3.8+

1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```bash
   python --version
   # Should show: Python 3.8.x or higher
   ```

### Node.js 16+

1. Download Node.js from: https://nodejs.org/
2. Install LTS version (recommended)
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Git (Optional but Recommended)

1. Download from: https://git-scm.com/
2. Install with default settings
3. Verify:
   ```bash
   git --version
   ```

## 2️⃣ Download the Project

### Option A: Clone with Git (Recommended)

```bash
git clone https://github.com/yourusername/cool-pwa-icon-generator.git
cd cool-pwa-icon-generator
```

### Option B: Download ZIP

1. Download ZIP from GitHub
2. Extract to desired location
3. Open terminal in extracted folder

## 3️⃣ Download AI Model Files

This is **CRITICAL** - the app won't work without these files!

### Required Files:

#### 1. LiberteRedmond.safetensors (~2GB)

- **Source**: HuggingFace
- **Direct Link**: https://huggingface.co/artificialguybr/Liberte/tree/main
- **Download**: Click on `LiberteRedmond.safetensors` file, then click the "download" button

#### 2. IconsRedmond15V-Icons.safetensors (~150MB)

- **Source**: CivitAI
- **Direct Link**: https://civitai.com/models/206191/iconsredmond-15v-app-icons-lora-for-sd-liberteredmond-sd-15
- **Download**: Click the blue "Download" button on the page to get the `.safetensors` file

### Where to Place Files:

**CRITICAL: Models must be in the project directory at:**
```
[project_folder]\models\
```

**Full file paths should be:**
```
[project_folder]\models\LiberteRedmond.safetensors
[project_folder]\models\IconsRedmond15V-Icons.safetensors
```

**NOT at:**
- ❌ g:\models\
- ❌ d:\models\
- ❌ Any other location

**Create the `models/` folder inside the project if it doesn't exist:**

```bash
# From the project directory ([project_folder])
mkdir models
```

**Verify the folder structure:**
```
[project_folder]\
├── models\                              ← Create this folder
│   ├── LiberteRedmond.safetensors      ← Place here
│   └── IconsRedmond15V-Icons.safetensors ← Place here
├── frontend\
├── main.py
├── config.py
└── ...other files
```

Then move/copy the downloaded `.safetensors` files into `[project_folder]\models\`.

## 4️⃣ Install Dependencies

### Windows - Automated Setup

**If using PowerShell (default in modern Windows):**
```powershell
.\start.bat
```

**If using Command Prompt (CMD):**
```cmd
start.bat
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Start both servers automatically
- ✅ Open browser to the app

### Manual Setup (All Platforms)

#### Backend (Python):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Frontend (Node.js):

```bash
cd frontend
npm install
cd ..
```

## 5️⃣ GPU Support (Optional but Recommended)

### Check GPU Compatibility

**NVIDIA GPU Required** (AMD/Intel not supported for GPU acceleration)

Check if you have CUDA-capable GPU:
```bash
nvidia-smi
```

If this works, you have an NVIDIA GPU!

### Install CUDA (for GPU Support)

1. Visit: https://developer.nvidia.com/cuda-downloads
2. Download CUDA Toolkit 11.8 or 12.1
3. Install with default settings
4. Restart computer

### Install PyTorch with CUDA

After CUDA installation:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Verify GPU Setup

```bash
python
>>> import torch
>>> torch.cuda.is_available()
True  # ← Should show True if GPU is working
>>> torch.cuda.get_device_name(0)
'NVIDIA GeForce RTX 3060'  # ← Your GPU name
>>> exit()
```

## 6️⃣ Start the Application

### Windows - Easy Start

```bash
start.bat
```

### Manual Start

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8088
- **API Documentation**: http://127.0.0.1:8088/docs

## 7️⃣ First Generation Test

1. Open http://localhost:3000
2. Enter test prompt: "A simple blue circle icon"
3. Settings:
   - Steps: 20 (fast)
   - Format: PNG
   - GPU: Check if available
4. Click "Generate All Icon Sizes"
5. Wait 10-15 seconds (GPU) or 60-90 seconds (CPU)
6. Icons should appear!

## 🏗️ How It Works - Single-Generation Architecture

**Important:** The Cool PWA Icon Generator uses an efficient **single-generation** architecture:

- ✅ AI generates **ONLY** the 512×512 base icon
- ✅ All other sizes (192×192, 180×180, 167×167, 152×152, 144×144, 128×128, 96×96, 72×72, 48×48, 32×32, 16×16) are created via **high-quality downscaling**
- ✅ This is ~2x faster than dual-generation approaches
- ✅ Ensures perfect consistency across all icon sizes
- ✅ Uses advanced Lanczos resampling for superior quality

**Generation Flow:**
1. AI generates 512×512 icon (~10-15s GPU / ~60-90s CPU)
2. Downscaler creates all other sizes instantly (<1s)
3. All icons delivered in single bundle

## ❗ Troubleshooting

### "Python not found"

**Solution:**
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH
- Restart terminal after installation

### "Node not found"

**Solution:**
- Reinstall Node.js
- Restart terminal
- Verify with `node --version`

### "Model files not found"

**Solution:**
```bash
# Check if files exist
ls models/
# Should show both .safetensors files

# If not, download them again
# Make sure filenames match exactly:
# - LiberteRedmond.safetensors
# - IconsRedmond15V-Icons.safetensors
```

### "CUDA out of memory"

**Solutions:**
1. Close other GPU-heavy applications
2. Use CPU mode instead (uncheck GPU in UI)
3. In `config.py`, set:
   ```python
   OFFLOAD_MODELS = True
   ```

### "Port already in use"

**Backend (8088):**
Edit `config.py`:
```python
PORT = 8089  # Change to any free port
```

**Frontend (3000):**
React will auto-suggest alternative port (3001, 3002, etc.)

### Slow Generation

**If using CPU:**
- This is normal! CPU mode is 5-6x slower than GPU
- 512×512 generation: ~60-90 seconds
- Downscaling all sizes: <1 second
- Total: ~60-90 seconds

**Solution:** Use GPU if available (reduces to ~10-15 seconds total)

### Poor Favicon Quality

**Issue:** 16×16 icons look blurry

**Solutions:**
- Use simpler prompts
- Add "minimalist, bold, high contrast" to prompt
- Avoid complex details
- Test: "A simple red circle" vs "A detailed dragon"

## 🎯 Next Steps

### Optimize Your Setup

1. **GPU Users:** Test both 20 and 50 steps to see quality difference
2. **CPU Users:** Stick with 20 steps for faster generation
3. **Test Prompts:** Try various styles to understand what works best

### Best Practices

**Good Prompts:**
- "A modern blue gradient app icon"
- "Simple green leaf icon, flat design"
- "Minimalist red heart logo"

**Avoid:**
- Complex scenes with many objects
- Text on icons
- Very detailed illustrations

### Learn More

- Read [ARCHITECTURE.md](docs-internal/ARCHITECTURE.md) for technical details
- Check [README.md](README.md) for full documentation
- Visit API docs: http://127.0.0.1:8088/docs

## 📊 Performance Expectations

### GPU Mode (NVIDIA RTX 3060)
- First generation: ~25s (loading model + generation)
- Subsequent generations: ~10-15s (AI) + <1s (downscaling)
- Quality (20 steps): Good
- Quality (50 steps): Excellent

### CPU Mode (Intel i7)
- First generation: ~90s (loading model + generation)
- Subsequent generations: ~60-90s (AI) + <1s (downscaling)
- Quality: Same as GPU
- Only difference: Speed

**Note:** All timing includes single 512×512 AI generation plus instant downscaling to all other sizes.

## 🆘 Getting Help

1. **Check Logs**: Look at terminal output for errors
2. **GitHub Issues**: https://github.com/yourusername/cool-pwa-icon-generator/issues
3. **Documentation**: Review README.md and ARCHITECTURE.md

## ✅ Setup Complete!

If you can generate icons successfully, you're all set! 

**Congratulations!** 🎉

Start creating amazing PWA icons with the Cool PWA Icon Generator!