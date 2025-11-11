@echo off
echo ================================================================================
echo BATCH PROCESSING - ALL INPUT FILES
echo ================================================================================
echo.
echo This will process ALL Excel files from test_input_files folder
echo and create timestamped outputs in batch_outputs folder
echo.
echo Press any key to continue...
pause >nul
echo.

REM Use Python 3.11 - it has all required packages
"C:\Users\Rajkumar\AppData\Local\Programs\Python\Python311\python.exe" batch_process_all_files.py

echo.
echo ================================================================================
echo BATCH PROCESSING COMPLETED
echo ================================================================================
echo.
echo Check batch_outputs folder for timestamped results
echo The summary HTML will open automatically in your browser
echo.
pause
