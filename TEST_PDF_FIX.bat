@echo off
echo ================================================================================
echo TESTING PDF FIX - Verifying Rock Solid Solution
echo ================================================================================
echo.

REM Step 1: Regenerate HTML with fixed templates
echo Step 1: Regenerating HTML files with fixed templates...
"C:\Users\Rajkumar\AppData\Local\Programs\Python\Python311\python.exe" -c "from core.computations.bill_processor import process_bill; from exports.renderers import generate_html; import pandas as pd; xl = pd.ExcelFile('test_input_files/SAMPLE BILL INPUT- NO EXTRA ITEMS.xlsx'); ws_wo = pd.read_excel(xl, 'Work Order', header=None); ws_bq = pd.read_excel(xl, 'Bill Quantity', header=None); ws_extra = pd.read_excel(xl, 'Extra Items', header=None); fp, lp, dev, ei, ns = process_bill(ws_wo, ws_bq, ws_extra, 5.0, 'above', 0); generate_html('first_page', fp, 'templates', 'TEST_OUTPUT'); generate_html('deviation_statement', dev, 'templates', 'TEST_OUTPUT'); generate_html('extra_items', ei, 'templates', 'TEST_OUTPUT'); print('HTML Generated')"

if not exist "TEST_OUTPUT" mkdir "TEST_OUTPUT"

echo.
echo Step 2: Generating PDFs with ANTI-SHRINK settings...
echo.

REM First Page
echo [1/3] first_page.pdf...
wkhtmltopdf --enable-local-file-access --page-size A4 --orientation Portrait --margin-top 10mm --margin-bottom 10mm --margin-left 10mm --margin-right 10mm --disable-smart-shrinking --zoom 1.0 --dpi 96 TEST_OUTPUT\first_page.html TEST_OUTPUT\first_page.pdf

REM Deviation Statement
echo [2/3] deviation_statement.pdf...
wkhtmltopdf --enable-local-file-access --page-size A4 --orientation Landscape --margin-top 10mm --margin-bottom 10mm --margin-left 10mm --margin-right 10mm --disable-smart-shrinking --zoom 1.0 --dpi 96 TEST_OUTPUT\deviation_statement.html TEST_OUTPUT\deviation_statement.pdf

REM Extra Items
echo [3/3] extra_items.pdf...
wkhtmltopdf --enable-local-file-access --page-size A4 --orientation Portrait --margin-top 10mm --margin-bottom 10mm --margin-left 10mm --margin-right 10mm --disable-smart-shrinking --zoom 1.0 --dpi 96 TEST_OUTPUT\extra_items.html TEST_OUTPUT\extra_items.pdf

echo.
echo ================================================================================
echo TEST COMPLETE!
echo ================================================================================
echo.
echo Generated files in TEST_OUTPUT folder:
dir /b TEST_OUTPUT
echo.
echo Opening PDFs for verification...
start "" "TEST_OUTPUT\first_page.pdf"
start "" "TEST_OUTPUT\deviation_statement.pdf"
start "" "TEST_OUTPUT\extra_items.pdf"
echo.
echo VERIFY:
echo   1. Tables are NOT shrunk
echo   2. All columns visible
echo   3. Margins exactly 10mm all around
echo   4. Text not cut off
echo.
pause
