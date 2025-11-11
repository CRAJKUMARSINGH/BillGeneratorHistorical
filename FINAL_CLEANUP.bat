@echo off
echo ================================================================================
echo FINAL CLEANUP - Removing Redundant Files and Folders
echo ================================================================================
echo.

REM Remove broken virtual environments
echo Removing broken virtual environments...
if exist ".venv_deploy" (
    rmdir /s /q ".venv_deploy"
    echo   Deleted: .venv_deploy
)
if exist "billgen_env" (
    rmdir /s /q "billgen_env"
    echo   Deleted: billgen_env
)

REM Remove redundant output folders
echo.
echo Removing redundant output folders...
if exist "All_Outputs" (
    rmdir /s /q "All_Outputs"
    echo   Deleted: All_Outputs
)

REM Remove Streamlit_Bill_Historical (archived work)
echo.
echo Removing archived Streamlit_Bill_Historical folder...
if exist "Streamlit_Bill_Historical" (
    rmdir /s /q "Streamlit_Bill_Historical"
    echo   Deleted: Streamlit_Bill_Historical
)

REM Remove Rajkumar_No_Doubt_Templates (if redundant)
echo.
echo Removing Rajkumar_No_Doubt_Templates folder...
if exist "Rajkumar_No_Doubt_Templates" (
    rmdir /s /q "Rajkumar_No_Doubt_Templates"
    echo   Deleted: Rajkumar_No_Doubt_Templates
)

REM Remove sample_bill.pdf (test file)
echo.
echo Removing test files...
if exist "sample_bill.pdf" (
    del /f /q "sample_bill.pdf"
    echo   Deleted: sample_bill.pdf
)

REM Clean test_outputs (keep folder, remove old files)
echo.
echo Cleaning test_outputs folder...
if exist "test_outputs\*.html" (
    del /f /q "test_outputs\*.html"
    echo   Cleaned: test_outputs HTML files
)
if exist "test_outputs\*.pdf" (
    del /f /q "test_outputs\*.pdf"
    echo   Cleaned: test_outputs PDF files
)
if exist "test_outputs\*.json" (
    del /f /q "test_outputs\*.json"
    echo   Cleaned: test_outputs JSON files
)
if exist "test_outputs\*.txt" (
    del /f /q "test_outputs\*.txt"
    echo   Cleaned: test_outputs TXT files
)
if exist "test_outputs\*.xlsx" (
    del /f /q "test_outputs\*.xlsx"
    echo   Cleaned: test_outputs XLSX files
)
if exist "test_outputs\*.md" (
    del /f /q "test_outputs\*.md"
    echo   Cleaned: test_outputs MD files
)

REM Remove test_outputs subdirectories
if exist "test_outputs\all_apps_test_*" (
    rmdir /s /q "test_outputs\all_apps_test_*"
    echo   Cleaned: test_outputs subdirectories
)
if exist "test_outputs\comprehensive_*" (
    rmdir /s /q "test_outputs\comprehensive_*"
    echo   Cleaned: test_outputs subdirectories
)
if exist "test_outputs\pdf_outputs" (
    rmdir /s /q "test_outputs\pdf_outputs"
    echo   Cleaned: test_outputs/pdf_outputs
)

echo.
echo ================================================================================
echo CLEANUP COMPLETE
echo ================================================================================
echo.
echo Removed:
echo   - Broken virtual environments (.venv_deploy, billgen_env)
echo   - Redundant output folders (All_Outputs)
echo   - Archived work (Streamlit_Bill_Historical)
echo   - Template archives (Rajkumar_No_Doubt_Templates)
echo   - Test files (sample_bill.pdf)
echo   - Old test outputs
echo.
echo Kept:
echo   - Core application (app/, core/, templates/, exports/)
echo   - Essential scripts (batch_process_all_files.py, run_interactive_bill_generation.py)
echo   - Documentation (README.md, PYTHON_SETUP_GUIDE.md, PDF_MASTER_GUIDE.md)
echo   - Test input files (test_input_files/)
echo   - Batch outputs (batch_outputs/)
echo   - Configuration (config/, .streamlit/)
echo.
pause
