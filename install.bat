@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════╗
echo ║   GitHydra Installation Script         ║
echo ║   نص تثبيت GitHydra                   ║
echo ╚════════════════════════════════════════╝
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    echo ❌ Python غير مثبت. يرجى تثبيت Python 3.11 أو أحدث.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%
echo ✅ تم العثور على Python %PYTHON_VERSION%
echo.

echo 📦 Installing GitHydra...
echo 📦 جاري تثبيت GitHydra...
echo.

if "%1"=="--dev" (
    echo 🔧 Installing in development mode...
    echo 🔧 التثبيت في وضع التطوير...
    pip install -e .
) else (
    echo 🚀 Installing GitHydra...
    echo 🚀 جاري تثبيت GitHydra...
    pip install .
)

if %errorlevel% equ 0 (
    echo.
    echo ╔════════════════════════════════════════╗
    echo ║  ✅ Installation Successful!          ║
    echo ║  ✅ تم التثبيت بنجاح!                 ║
    echo ╚════════════════════════════════════════╝
    echo.
    echo 🎯 Quick Start / البداية السريعة:
    echo.
    echo    githydra interactive     # Interactive mode / الوضع التفاعلي
    echo    githydra --help          # Show help / عرض المساعدة
    echo    githydra status          # Check status / فحص الحالة
    echo.
    echo 📚 For more information, see README.md
    echo 📚 لمزيد من المعلومات، انظر README.md
) else (
    echo.
    echo ❌ Installation failed. Please check the error messages above.
    echo ❌ فشل التثبيت. يرجى التحقق من رسائل الخطأ أعلاه.
    pause
    exit /b 1
)

pause
