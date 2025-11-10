@echo off
REM Archive Stream Bill Apps - Simple Batch Script
REM This will safely copy all 7 apps to an archive folder

echo.
echo ================================================================================
echo                    STREAM BILL APPS - ARCHIVE SCRIPT
echo ================================================================================
echo.
echo This will archive (copy) 7 apps to a safe location.
echo.
echo KEEP: Stream-Bill-App_Main
echo ARCHIVE: 7 other apps
echo.
echo Archive Location: C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED
echo.
echo ================================================================================
echo.

pause

echo.
echo Creating archive folder...
mkdir "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED" 2>nul
echo Done!
echo.

echo ================================================================================
echo Archiving apps... (This may take 5-10 minutes)
echo ================================================================================
echo.

echo [1/7] Archiving Stream-Bill-FIRST-ONE...
xcopy "C:\Users\Rajkumar\Stream-Bill-FIRST-ONE" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-FIRST-ONE\" /E /I /H /Y
echo Done!
echo.

echo [2/7] Archiving Stream-Bill-Generator-SAPNA...
xcopy "C:\Users\Rajkumar\Stream-Bill-Generator-SAPNA" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-Generator-SAPNA\" /E /I /H /Y
echo Done!
echo.

echo [3/7] Archiving Stream-Bill-INIT-PY...
xcopy "C:\Users\Rajkumar\Stream-Bill-INIT-PY" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-INIT-PY\" /E /I /H /Y
echo Done!
echo.

echo [4/7] Archiving Stream-Bill-generator-main...
xcopy "C:\Users\Rajkumar\Stream-Bill-generator-main" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-generator-main\" /E /I /H /Y
echo Done!
echo.

echo [5/7] Archiving Stream-Bill-generator-main2...
xcopy "C:\Users\Rajkumar\Stream-Bill-generator-main2" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Stream-Bill-generator-main2\" /E /I /H /Y
echo Done!
echo.

echo [6/7] Archiving Streamlit_Bill_Historical...
xcopy "C:\Users\Rajkumar\Streamlit_Bill_Historical" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Streamlit_Bill_Historical\" /E /I /H /Y
echo Done!
echo.

echo [7/7] Archiving Streamlit_Bill_New...
xcopy "C:\Users\Rajkumar\Streamlit_Bill_New" "C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED\Streamlit_Bill_New\" /E /I /H /Y
echo Done!
echo.

echo ================================================================================
echo                           ARCHIVING COMPLETE!
echo ================================================================================
echo.
echo All 7 apps have been archived to:
echo C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED
echo.
echo Original folders are still in place.
echo.
echo NEXT STEPS:
echo 1. Verify archive: dir C:\Users\Rajkumar\Stream-Bill-Apps-ARCHIVED
echo 2. Test main app: cd Stream-Bill-App_Main
echo 3. Run tests: python scripts\test_pdf_generation_comprehensive.py
echo 4. After 1 week, you can delete original folders if everything works
echo.
echo ================================================================================
echo.

pause
