@echo off
REM push.bat - Trigger immediate git push for Windows

echo 🚀 Triggering immediate git push...
echo ======================================

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python script exists
if not exist "git_auto_simple.py" (
    echo ❌ Error: git_auto_simple.py not found!
    echo Please make sure the file exists in the current directory.
    pause
    exit /b 1
)

REM Check if virtual environment is active (optional)
if not "%VIRTUAL_ENV%"=="" (
    echo ✓ Virtual environment detected
)

REM Run the Python script
echo 📦 Checking for changes and pushing to git...
echo ----------------------------------------------

python git_auto_simple.py

set EXIT_CODE=%errorlevel%

echo ----------------------------------------------

if %EXIT_CODE% equ 0 (
    echo ✅ Push completed successfully!
) else (
    echo ❌ Push failed with exit code: %EXIT_CODE%
)

pause
exit /b %EXIT_CODE%

