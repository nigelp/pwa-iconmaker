@echo off
setlocal enabledelayedexpansion
echo ========================================
echo Cool PWA Icon Generator - Installation
echo Offline AI-Powered Icon Maker
echo ========================================
echo.
echo This script will set up the development environment.
echo It will NOT start the servers (use start.bat for that).
echo.
pause

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version
echo Python found!
echo.

REM Check if Node.js is installed
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo.
    echo Please install Node.js from:
    echo https://nodejs.org/
    pause
    exit /b 1
)
node --version
npm --version
echo Node.js found!
echo.

REM Detect GPU
echo [3/6] Detecting GPU capabilities...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo NVIDIA GPU detected - will install CUDA support
    set GPU_MODE=cuda
) else (
    echo No NVIDIA GPU detected - will install CPU-only version
    set GPU_MODE=cpu
)
echo.

REM Create Python virtual environment
echo [4/6] Setting up Python virtual environment...
if exist "venv" (
    echo Virtual environment already exists, skipping creation...
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install Python dependencies
echo [5/6] Installing Python dependencies...
echo This may take several minutes (downloading ~4GB of packages)...
echo.

if "!GPU_MODE!"=="cuda" (
    echo Installing PyTorch with CUDA 12.8 support...
    python -m pip install --quiet --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
    if %errorlevel% neq 0 (
        echo WARNING: CUDA installation failed, falling back to CPU version
        python -m pip install --quiet torch torchvision torchaudio
    )
) else (
    echo Installing PyTorch (CPU version)...
    python -m pip install --quiet torch torchvision torchaudio
)

echo.
echo Installing FastAPI, Stable Diffusion, and other dependencies...
python -m pip install --quiet -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo Python dependencies installed successfully!
echo.

REM Install Node.js dependencies
echo [6/6] Installing Node.js dependencies for frontend...
cd frontend
if exist "node_modules" (
    echo Node modules already exist, skipping installation...
) else (
    echo Installing React and frontend dependencies...
    call npm install --loglevel=error
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Node.js dependencies
        cd ..
        pause
        exit /b 1
    )
    echo Frontend dependencies installed successfully!
)
cd ..

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Download AI models (see MODELS_DOWNLOAD.md)
echo 2. Place models in: [project_folder]\models\
echo 3. Run start.bat to launch the application
echo.
echo Model files needed:
echo - LiberteRedmond.safetensors (~3.5GB)
echo - IconsRedmond15V-Icons.safetensors (~3.5GB)
echo.
echo For detailed instructions, see:
echo - README.md (Quick start guide)
echo - SETUP_GUIDE.md (Complete setup guide)
echo - MODELS_DOWNLOAD.md (Model download links)
echo.
pause