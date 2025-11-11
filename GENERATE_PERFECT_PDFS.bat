@echo off
echo ================================================================================
echo GENERATE PERFECT PDFs - No Shrinking, Perfect Tables
echo ================================================================================
echo.

set "BATCH_DIR=batch_outputs\20251111_130315_sample_bill_input_no_extra_items"

if not exist "%BATCH_DIR%" (
    echo ERROR: Batch directory not found!
    echo Please run batch_process_all_files.py first
    pause
    exit /b 1
)

echo Generating PDFs with anti-shrinking options...
echo.

REM First Page (Portrait)
echo [1/3] Generating first_page.pdf...
wkhtmltopdf ^
  --enable-local-file-access ^
  --page-size A4 ^
  --margin-top 10mm ^
  --margin-bottom 10mm ^
  --margin-left 10mm ^
  --margin-right 10mm ^
  --orientation Portrait ^
  --disable-smart-shrinking ^
  --zoom 1.0 ^
  --dpi 96 ^
  --no-pdf-compression ^
  "%BATCH_DIR%\first_page.html" ^
  "%BATCH_DIR%\first_page_PERFECT.pdf"

if exist "%BATCH_DIR%\first_page_PERFECT.pdf" (
    echo   [OK] first_page_PERFECT.pdf generated
) else (
    echo   [ERROR] Failed to generate first_page_PERFECT.pdf
)

REM Deviation Statement (Landscape)
echo [2/3] Generating deviation_statement.pdf...
wkhtmltopdf ^
  --enable-local-file-access ^
  --page-size A4 ^
  --margin-top 10mm ^
  --margin-bottom 10mm ^
  --margin-left 10mm ^
  --margin-right 10mm ^
  --orientation Landscape ^
  --disable-smart-shrinking ^
  --zoom 1.0 ^
  --dpi 96 ^
  --no-pdf-compression ^
  "%BATCH_DIR%\deviation_statement.html" ^
  "%BATCH_DIR%\deviation_statement_PERFECT.pdf"

if exist "%BATCH_DIR%\deviation_statement_PERFECT.pdf" (
    echo   [OK] deviation_statement_PERFECT.pdf generated
) else (
    echo   [ERROR] Failed to generate deviation_statement_PERFECT.pdf
)

REM Extra Items (Portrait)
echo [3/3] Generating extra_items.pdf...
wkhtmltopdf ^
  --enable-local-file-access ^
  --page-size A4 ^
  --margin-top 10mm ^
  --margin-bottom 10mm ^
  --margin-left 10mm ^
  --margin-right 10mm ^
  --orientation Portrait ^
  --disable-smart-shrinking ^
  --zoom 1.0 ^
  --dpi 96 ^
  --no-pdf-compression ^
  "%BATCH_DIR%\extra_items.html" ^
  "%BATCH_DIR%\extra_items_PERFECT.pdf"

if exist "%BATCH_DIR%\extra_items_PERFECT.pdf" (
    echo   [OK] extra_items_PERFECT.pdf generated
) else (
    echo   [ERROR] Failed to generate extra_items_PERFECT.pdf
)

echo.
echo ================================================================================
echo PDF GENERATION COMPLETE
echo ================================================================================
echo.
echo Generated PDFs with:
echo   - 10mm margins all around
echo   - NO smart shrinking (--disable-smart-shrinking)
echo   - Fixed zoom at 1.0 (--zoom 1.0)
echo   - Standard DPI 96 (--dpi 96)
echo   - No compression for better quality
echo.
echo Location: %BATCH_DIR%\
echo.
echo Opening PDFs...
start "" "%BATCH_DIR%\first_page_PERFECT.pdf"
start "" "%BATCH_DIR%\deviation_statement_PERFECT.pdf"
start "" "%BATCH_DIR%\extra_items_PERFECT.pdf"
echo.
pause
