@echo off
echo ================================================================================
echo ULTIMATE PDF GENERATION - ROCK SOLID SOLUTION
echo ================================================================================
echo.
echo This will generate PDFs with ZERO shrinking and PERFECT table widths
echo.

set HTML_DIR=batch_outputs\20251111_130315_sample_bill_input_no_extra_items
set OUTPUT_DIR=PERFECT_PDFS

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo Generating first_page.pdf...
wkhtmltopdf ^
    --enable-local-file-access ^
    --page-size A4 ^
    --orientation Portrait ^
    --margin-top 10mm ^
    --margin-bottom 10mm ^
    --margin-left 10mm ^
    --margin-right 10mm ^
    --disable-smart-shrinking ^
    --zoom 1.0 ^
    --dpi 96 ^
    --image-quality 100 ^
    --no-background ^
    "%HTML_DIR%\first_page.html" ^
    "%OUTPUT_DIR%\first_page.pdf"

echo.
echo Generating deviation_statement.pdf...
wkhtmltopdf ^
    --enable-local-file-access ^
    --page-size A4 ^
    --orientation Landscape ^
    --margin-top 10mm ^
    --margin-bottom 10mm ^
    --margin-left 10mm ^
    --margin-right 10mm ^
    --disable-smart-shrinking ^
    --zoom 1.0 ^
    --dpi 96 ^
    --image-quality 100 ^
    --no-background ^
    "%HTML_DIR%\deviation_statement.html" ^
    "%OUTPUT_DIR%\deviation_statement.pdf"

echo.
echo Generating extra_items.pdf...
wkhtmltopdf ^
    --enable-local-file-access ^
    --page-size A4 ^
    --orientation Portrait ^
    --margin-top 10mm ^
    --margin-bottom 10mm ^
    --margin-left 10mm ^
    --margin-right 10mm ^
    --disable-smart-shrinking ^
    --zoom 1.0 ^
    --dpi 96 ^
    --image-quality 100 ^
    --no-background ^
    "%HTML_DIR%\extra_items.html" ^
    "%OUTPUT_DIR%\extra_items.pdf"

echo.
echo ================================================================================
echo PERFECT PDFs GENERATED!
echo ================================================================================
echo.
echo Location: %OUTPUT_DIR%\
echo.
echo Key Features:
echo   - 10mm margins all around
echo   - NO shrinking (--disable-smart-shrinking)
echo   - Fixed zoom at 1.0
echo   - DPI set to 96 for perfect rendering
echo   - Tables maintain exact widths
echo.
echo Opening PDFs...
start "" "%OUTPUT_DIR%\first_page.pdf"
start "" "%OUTPUT_DIR%\deviation_statement.pdf"
start "" "%OUTPUT_DIR%\extra_items.pdf"
echo.
pause
