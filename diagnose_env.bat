@echo off
echo ====================================
echo Environment Diagnostic Test
echo ====================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [TEST 1] Python Location:
where python
echo.

echo [TEST 2] Pip Location:
where pip
echo.

echo [TEST 3] Pip3 Location (if exists):
where pip3 2>nul
if %errorlevel% neq 0 (
    echo pip3 not found in PATH
)
echo.

echo [TEST 4] Installed Packages:
pip list | findstr /i "fastapi torch"
echo.

echo [TEST 5] Python Environment Path:
python -c "import sys; print('\n'.join(sys.path))"
echo.

echo ====================================
echo Diagnostic Complete
echo ====================================
pause