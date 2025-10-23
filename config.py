"""
Configuration settings for Cool PWA Icon Generator
Offline AI-Powered Progressive Web App Icon Maker
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent  # g:\newlocalicons
MODELS_DIR = BASE_DIR / "models"  # g:\newlocalicons\models
TEMP_DIR = BASE_DIR / "temp"      # g:\newlocalicons\temp
STATIC_DIR = BASE_DIR / "static"  # g:\newlocalicons\static

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Model Configuration
MODEL_BASE = "runwayml/stable-diffusion-v1-5"
LORA_MODELS = {
    "liberte": MODELS_DIR / "LiberteRedmond.safetensors",
    "icons": MODELS_DIR / "IconsRedmond15V-Icons.safetensors"
}

# Generation Settings
DEFAULT_STEPS = 20
AVAILABLE_STEPS = [20, 50]
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_SEED = None  # None for random seed

# Icon Sizes (PWA Standard)
# Optimized architecture: Generate only 512x512, resize all other sizes
ICON_SIZES = {
    "large": 512,      # AI-generated master image
    "medium": 192,     # Downscaled from 512 (2.67x)
    "small": 164,      # Downscaled from 512 (3.1x)
    "favicon": 16      # Downscaled from 512 (32x) with extra sharpening
}

# Image Quality Settings
DOWNSCALE_METHOD = "LANCZOS"  # High-quality resampling
SHARPEN_SMALL_ICONS = True
SHARPEN_RADIUS = 1
SHARPEN_PERCENT = 150
SHARPEN_THRESHOLD = 3

# Output Formats
AVAILABLE_FORMATS = ["png", "jpeg"]
DEFAULT_FORMAT = "png"

# Server Settings
HOST = "127.0.0.1"
PORT = 8088
RELOAD = True  # Development mode

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    f"http://{HOST}:{PORT}"
]

# Generation Limits
MAX_CONCURRENT_GENERATIONS = 1
TEMP_FILE_RETENTION_HOURS = 1
MAX_ZIP_SIZE_MB = 10

# Prompt Enhancement
# CRITICAL: Force AI to generate large icons that fill the frame with minimal padding
# "icons" tag activates LORA fine-tuning for better quality
ICON_PROMPT_SUFFIX = ", app icon design, ZOOMED IN, CLOSE UP VIEW, fills entire frame, edge to edge, large scale, no padding, no margins, centered, flat design, simple, clean, professional, solid color background"
SMALL_ICON_PROMPT_SUFFIX = ", app icon design, ZOOMED IN, CLOSE UP VIEW, fills entire frame, large scale, no padding, minimalist, bold, high contrast, simple shapes"
LORA_BASE_TAG = "icons"  # Activates LORA - must be included in all prompts

# Memory Management
SEQUENTIAL_GENERATION = True  # Generate one at a time to manage memory
OFFLOAD_MODELS = False  # Set True for low-VRAM GPUs