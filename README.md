# 🎨 Cool PWA Icon Generator

<img width="474" height="305" alt="pwagrab5-small" src="https://github.com/user-attachments/assets/b7866ac7-095e-4164-907a-cd1a33a1ae13" />


**Offline AI-Powered Progressive Web App Icon Maker**

(Check out my other cool tools and utilities at https://www.dollarware.net. Some free, some not. :) 

Generate beautiful, professional PWA icons using local AI models - completely offline, no API keys required. Generate all four required PWA icon sizes from a single prompt with consistent design across all resolutions.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-14%2B-green)](https://nodejs.org/)

---

## ✨ Features

- **🤖 Local AI Generation** - Uses Stable Diffusion with custom LoRA fine-tuning for professional icon design
- **📦 Complete PWA Icon Suite** - Generates all 4 required sizes: 512×512, 192×192, 164×164, and 16×16 (favicon)
- **🎯 Single-Pass Architecture** - Generates one high-quality 512×512 master icon, then creates all other sizes via intelligent downscaling
- **✨ Adaptive Sharpening** - Size-specific sharpening ensures crisp, clear icons at every resolution
- **💾 Multiple Formats** - Export as PNG, JPEG, or ICO (for favicon)
- **📥 Instant Downloads** - Download individual icons or complete ZIP bundle with manifest.json template
- **🔒 100% Offline** - No API keys, no cloud services, complete privacy
- **⚡ GPU Accelerated** - CUDA support for fast generation (CPU fallback available)

---

## 🏗️ Architecture

### Generation Pipeline

```
User Prompt → AI Model (512×512) → High-Quality Downscaling → 4 PWA Icon Sizes
                                           ↓
                                  Adaptive Sharpening
                                  LANCZOS Resampling
```

**Key Design Principles:**
1. **Single AI Generation Pass** - Generate one 512×512 master icon for perfect consistency
2. **Intelligent Downscaling** - Advanced LANCZOS resampling with adaptive sharpening
3. **Size-Optimized Processing** - Different sharpening intensity based on downscale ratio
4. **Format Flexibility** - Automatic ICO conversion for favicons

### Icon Sizes Generated

| Size | Purpose | Generation Method |
|------|---------|-------------------|
| **512×512** | Large icon (app launcher, splash screen) | AI-generated master image |
| **192×192** | Medium icon (home screen, app launcher) | Downscaled from 512×512 |
| **164×164** | Small icon (UI elements) | Downscaled from 512×512 |
| **16×16** | Favicon (browser tabs) | Downscaled from 512×512, exported as ICO |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **~7GB disk space** - For AI models
- **NVIDIA GPU** (optional) - For faster generation

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cool-pwa-icon-generator.git
   cd cool-pwa-icon-generator
   ```

2. **Download AI models** (see [MODELS_DOWNLOAD.md](MODELS_DOWNLOAD.md)):
   - Place model files in `[project_folder]/models/` directory
   - Required: `LiberteRedmond.safetensors` (~3.5GB)
   - Required: `IconsRedmond15V-Icons.safetensors` (~3.5GB)

3. **Run the installer:**
   ```bash
   # Windows
   INSTALL.bat
   
   # This will:
   # - Create Python virtual environment
   # - Install all dependencies (PyTorch, FastAPI, Stable Diffusion, etc.)
   # - Set up frontend dependencies
   ```

4. **Start the application:**
   ```bash
   # Windows
   start.bat
   
   # The app will automatically:
   # - Start backend API server (http://127.0.0.1:8088)
   # - Start React frontend (http://localhost:3000)
   # - Open your browser at http://localhost:3000
   ```

5. **Generate your first icon:**
   - Enter a prompt (e.g., "A modern blue gradient rocket icon")
   - Click "Generate Icons"
   - Download individual icons or complete ZIP bundle

---

## 📖 Detailed Setup Guide

For comprehensive installation instructions, troubleshooting, and configuration options, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

---

## 💻 System Requirements

### Minimum Requirements (CPU-only)
- **OS:** Windows 10/11, Linux, macOS
- **CPU:** 4+ cores
- **RAM:** 16GB
- **Disk:** 10GB free space
- **Generation time:** ~30-60 seconds per icon set

### Recommended (GPU-accelerated)
- **OS:** Windows 10/11, Linux
- **GPU:** NVIDIA GPU with 6GB+ VRAM (GTX 1060 6GB or better)
- **CUDA:** 11.8 or 12.1
- **RAM:** 16GB+
- **Disk:** 10GB free space (SSD recommended)
- **Generation time:** ~5-10 seconds per icon set

---

## 🎨 Usage Examples

### Basic Icon Generation
```
Prompt: "colorful kettle"
Steps: 20 (fast) or 50 (high quality)
Format: PNG (recommended) or JPEG
```

### Advanced Prompts
```
"vintage blue car"
"detailed finance app"
"weather app minimalism"
```

### Tips for Best Results
- Be specific about color and style
- Use descriptive adjectives (modern, minimalist, detailed, etc.)
- Specify design style (flat, gradient, 3D, etc.)
- Try to keep your prompts as simple as possible, but make sure to experiment
- Remember this is a local model, so it may take quite a few tries to get something you like! 

---

## 📁 Project Structure

```
cool-pwa-icon-generator/
├── README.md                 # This file
├── SETUP_GUIDE.md           # Detailed setup instructions
├── MODELS_DOWNLOAD.md       # AI model download guide
├── LICENSE                  # Apache 2.0 License
├── requirements.txt         # Python dependencies
├── INSTALL.bat             # One-click installer (Windows)
├── start.bat               # One-click startup (Windows)
├── config.py               # Application configuration
├── main.py                 # FastAPI backend server
├── icon_generator.py       # AI generation engine
├── image_processor.py      # Image processing & downscaling
├── zip_bundler.py          # ZIP bundle creation
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── ...
│   ├── public/
│   └── package.json
├── models/                 # AI models directory (gitignored)
│   ├── LiberteRedmond.safetensors
│   └── IconsRedmond15V-Icons.safetensors
└── tests/                  # Test suite
```

---

## 🔧 Configuration

Edit `config.py` to customize:

- **Server settings:** Host, port, CORS origins
- **AI model paths:** Custom model locations
- **Generation parameters:** Default steps, guidance scale
- **Image processing:** Sharpening intensity, quality settings
- **Cache settings:** Temporary file retention

---

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'fastapi'"**
- Run `INSTALL.bat` to install all dependencies
- Ensure you're using the virtual environment

**"CUDA out of memory"**
- Reduce image size in config.py
- Use CPU mode by unchecking "Use GPU" in UI
- Close other GPU-intensive applications

**Models not found**
- Check `[project_folder]/models/` directory
- Download models from links in MODELS_DOWNLOAD.md
- Ensure filenames match exactly: `LiberteRedmond.safetensors` and `IconsRedmond15V-Icons.safetensors`

**Slow generation on CPU**
- CPU generation is normal - takes 30-60 seconds
- Consider using GPU for 5-10 second generation
- Reduce steps to 20 for faster (but slightly lower quality) results

For more troubleshooting tips, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stable Diffusion** - Core AI image generation
- **FastAPI** - High-performance backend framework
- **React** - Modern frontend framework
- **Pillow (PIL)** - Image processing library
- **PyTorch** - Deep learning framework

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/cool-pwa-icon-generator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/cool-pwa-icon-generator/discussions)

---

**Made with ❤️ for the PWA community**
