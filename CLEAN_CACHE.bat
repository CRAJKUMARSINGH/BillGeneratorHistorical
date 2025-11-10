@echo off
REM Clean All Caches - Quick Batch Script

echo.
echo ================================================================================
echo                         CACHE CLEANING UTILITY
echo ================================================================================
echo.
echo This will clean:
echo   - Python cache (__pycache__, .pyc files)
echo   - PDF generation cache
echo   - Temporary files (.tmp, .log, .bak)
echo   - Old test outputs (keeps 3 most recent)
echo.
echo ================================================================================
echo.

pause

echo.
echo Cleaning Python cache...
echo.

REM Remove __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Removing: %%d
    rd /s /q "%%d"
)

REM Remove .pyc files
for /r . %%f in (*.pyc) do @if exist "%%f" (
    echo Removing: %%f
    del /q "%%f"
)

echo.
echo Cleaning temporary files...
echo.

REM Remove temporary files
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *.bak 2>nul
del /s /q *.backup 2>nul

echo.
echo Running Python cache cleaner...
echo.

python scripts\clean_cache.py

echo.
echo ================================================================================
echo                         CACHE CLEANING COMPLETE!
echo ================================================================================
echo.

pause
