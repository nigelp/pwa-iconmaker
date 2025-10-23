@echo off
setlocal enabledelayedexpansion
echo ====================================
echo Cool PWA Icon Generator - Starting...
echo Offline AI-Powered Icon Maker
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from nodejs.org
    pause
    exit /b 1
)

echo [1/5] Detecting GPU...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo NVIDIA GPU detected - will install CUDA support
    set GPU_MODE=cuda
) else (
    echo No NVIDIA GPU - will install CPU-only version
    set GPU_MODE=cpu
)
echo.

echo [2/5] Setting up Python environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

echo [3/5] Installing dependencies...
echo This may take several minutes...
echo.

if "!GPU_MODE!"=="cuda" (
    echo Installing PyTorch with CUDA 12.8...
    python -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
) else (
    echo Installing PyTorch CPU version...
    python -m pip install torch torchvision torchaudio
)

echo.
echo Installing FastAPI and other dependencies...
python -m pip install -r requirements.txt

echo.
echo [4/5] Checking Frontend dependencies...
cd frontend
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)
cd ..

echo.
echo [5/5] Starting servers...
start "Backend - FastAPI" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && python main.py"

timeout /t 5 /nobreak >nul

start "Frontend - React" cmd /k "cd /d "%~dp0frontend" && npm start"

echo.
echo ====================================
echo Started Successfully!
echo ====================================
echo.
if "!GPU_MODE!"=="cuda" (
    echo Mode: GPU Acceleration
    echo Generation time: ~10-15 seconds
) else (
    echo Mode: CPU Only
    echo Generation time: ~90-140 seconds
)
echo.
echo Frontend: http://localhost:3000
echo Backend: http://127.0.0.1:8088
echo.
echo Download model files from README.md links
echo Place in: models folder
echo.
pause