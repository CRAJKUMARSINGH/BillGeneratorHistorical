@echo off
title Stream Bill Generator - Basic Version

echo ====================================================
echo STREAM BILL GENERATOR - BASIC VERSION
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Checking required packages...
python -c "import streamlit, pandas, pdfkit, docx, num2words, jinja2, pypdf, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Required packages not found. Please run INSTALL_REQUIREMENTS.bat first.
    pause
    exit /b 1
)

echo Starting Streamlit server...
echo.
echo The app will be available at: http://localhost:8503
echo.
echo Close this window to stop the server
echo.

python -m streamlit run app/main.py --server.port 8503

pause