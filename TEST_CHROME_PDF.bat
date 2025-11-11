@echo off
echo ================================================================================
echo CHROME HEADLESS PDF GENERATION - ULTIMATE SOLUTION
echo ================================================================================
echo.

set HTML_DIR=batch_outputs\20251111_130315_sample_bill_input_no_extra_items
set OUTPUT_DIR=CHROME_PDFS

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Find Chrome
set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist %CHROME% set CHROME="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

echo Using Chrome: %CHROME%
echo.

echo [1/3] Generating first_page.pdf with Chrome...
%CHROME% --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf="%OUTPUT_DIR%\first_page.pdf" "%HTML_DIR%\first_page.html"

echo [2/3] Generating deviation_statement.pdf with Chrome...
%CHROME% --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf="%OUTPUT_DIR%\deviation_statement.pdf" "%HTML_DIR%\deviation_statement.html"

echo [3/3] Generating extra_items.pdf with Chrome...
%CHROME% --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf="%OUTPUT_DIR%\extra_items.pdf" "%HTML_DIR%\extra_items.html"

echo.
echo ================================================================================
echo CHROME PDFs GENERATED!
echo ================================================================================
echo.
echo Location: %OUTPUT_DIR%\
echo.
echo Chrome Advantages:
echo   - NO shrinking (--disable-smart-shrinking)
echo   - Perfect CSS rendering
echo   - Exact table widths maintained
echo   - Modern rendering engine
echo   - No external dependencies
echo.
dir /b "%OUTPUT_DIR%"
echo.
echo Opening PDFs...
start "" "%OUTPUT_DIR%\first_page.pdf"
start "" "%OUTPUT_DIR%\deviation_statement.pdf"
start "" "%OUTPUT_DIR%\extra_items.pdf"
echo.
pause
