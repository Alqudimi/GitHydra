#!/bin/bash

echo "╔════════════════════════════════════════╗"
echo "║   GitHydra Installation Script         ║"
echo "║   نص تثبيت GitHydra                   ║"
echo "╚════════════════════════════════════════╝"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.11 أو أحدث."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo "✅ تم العثور على Python $PYTHON_VERSION"
echo ""

echo "📦 Installing GitHydra..."
echo "📦 جاري تثبيت GitHydra..."
echo ""

if [ "$1" == "--dev" ]; then
    echo "🔧 Installing in development mode..."
    echo "🔧 التثبيت في وضع التطوير..."
    pip install -e .
else
    echo "🚀 Installing GitHydra..."
    echo "🚀 جاري تثبيت GitHydra..."
    pip install .
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║  ✅ Installation Successful!          ║"
    echo "║  ✅ تم التثبيت بنجاح!                 ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    echo "🎯 Quick Start / البداية السريعة:"
    echo ""
    echo "   githydra interactive     # Interactive mode / الوضع التفاعلي"
    echo "   githydra --help          # Show help / عرض المساعدة"
    echo "   githydra status          # Check status / فحص الحالة"
    echo ""
    echo "📚 For more information, see README.md"
    echo "📚 لمزيد من المعلومات، انظر README.md"
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    echo "❌ فشل التثبيت. يرجى التحقق من رسائل الخطأ أعلاه."
    exit 1
fi
