# دليل التثبيت - GitHydra

<div dir="rtl">

## المتطلبات الأساسية

قبل تثبيت GitHydra، تأكد من توفر ما يلي:

### 1. Python
- **الإصدار المطلوب:** Python 3.11 أو أحدث
- **التحقق من التثبيت:**
```bash
python --version
# أو
python3 --version
```

### 2. Git
- **الإصدار المطلوب:** Git 2.0 أو أحدث
- **التحقق من التثبيت:**
```bash
git --version
```

### 3. pip
- مدير حزم Python (يأتي مع Python)
- **التحقق من التثبيت:**
```bash
pip --version
# أو
pip3 --version
```

## طرق التثبيت

### الطريقة 1: التثبيت عبر pip (موصى به)

#### الخطوة 1: استنساخ المستودع
```bash
git clone https://github.com/Alqudimi/GitHydra.git
cd GitHydra
```

#### الخطوة 2: التثبيت
```bash
pip install -e .
```

#### الخطوة 3: التحقق من التثبيت
```bash
githydra --version
githydra --help
```

### الطريقة 2: استخدام سكريبت التثبيت

#### على Linux/macOS
```bash
# استنساخ المستودع
git clone https://github.com/Alqudimi/GitHydra.git
cd GitHydra

# إعطاء صلاحيات التنفيذ
chmod +x install.sh

# تشغيل سكريبت التثبيت
./install.sh
```

#### على Windows
```cmd
# استنساخ المستودع
git clone https://github.com/Alqudimi/GitHydra.git
cd GitHydra

# تشغيل سكريبت التثبيت
install.bat
```

### الطريقة 3: التثبيت اليدوي

#### الخطوة 1: استنساخ المستودع
```bash
git clone https://github.com/Alqudimi/GitHydra.git
cd GitHydra
```

#### الخطوة 2: تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

#### الخطوة 3: إضافة المسار إلى PATH (اختياري)
```bash
# على Linux/macOS (أضف إلى ~/.bashrc أو ~/.zshrc)
export PATH="$PATH:/path/to/GitHydra"

# على Windows (أضف إلى متغيرات البيئة)
# يمكن إضافة المسار عبر إعدادات النظام
```

## التحقق من التثبيت الناجح

بعد التثبيت، تحقق من أن GitHydra يعمل بشكل صحيح:

### 1. التحقق من الإصدار
```bash
githydra --version
```

### 2. عرض المساعدة
```bash
githydra --help
```

### 3. تشغيل الوضع التفاعلي
```bash
githydra interactive
```

### 4. اختبار أمر بسيط
```bash
githydra status
```

## حل المشاكل الشائعة

### المشكلة 1: "githydra: command not found"

**الحل:**
```bash
# تأكد من أن pip يثبت في المسار الصحيح
pip install --user -e .

# أو أضف مسار Python إلى PATH
export PATH="$PATH:$HOME/.local/bin"
```

### المشكلة 2: أخطاء الأذونات على Linux/macOS

**الحل:**
```bash
# استخدم --user flag
pip install --user -e .

# أو استخدم virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

### المشكلة 3: "No module named 'rich'"

**الحل:**
```bash
# تثبيت المتطلبات يدوياً
pip install rich click gitpython questionary pyyaml colorama
```

### المشكلة 4: مشاكل Python 3.11

**الحل:**
```bash
# استخدم pyenv لتثبيت Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0
```

## التثبيت في بيئة افتراضية (Virtual Environment)

يُنصح باستخدام بيئة افتراضية لعزل المتطلبات:

### على Linux/macOS
```bash
# إنشاء بيئة افتراضية
python -m venv githydra-env

# تفعيل البيئة
source githydra-env/bin/activate

# التثبيت
pip install -e .
```

### على Windows
```cmd
# إنشاء بيئة افتراضية
python -m venv githydra-env

# تفعيل البيئة
githydra-env\Scripts\activate

# التثبيت
pip install -e .
```

## الترقية

لترقية GitHydra إلى أحدث إصدار:

```bash
# الانتقال إلى مجلد المشروع
cd GitHydra

# سحب آخر التحديثات
git pull origin main

# إعادة التثبيت
pip install -e . --upgrade
```

## إلغاء التثبيت

لإزالة GitHydra من النظام:

```bash
pip uninstall githydra
```

## التكوين الأولي

بعد التثبيت، قم بتكوين GitHydra:

### 1. إعداد Git (إن لم يكن مُعداً)
```bash
git config --global user.name "اسمك"
git config --global user.email "your.email@example.com"
```

### 2. تشغيل GitHydra لأول مرة
```bash
githydra interactive
```

سيقوم GitHydra تلقائياً بإنشاء ملفات التكوين في `~/.githydra/`:
- `config.yaml` - إعدادات المستخدم
- `aliases.yaml` - الأوامر المختصرة
- `logs/` - مجلد السجلات

## متطلبات النظام

### الحد الأدنى
- **المعالج:** 1 GHz أو أعلى
- **الذاكرة:** 512 MB RAM
- **المساحة:** 50 MB مساحة حرة
- **نظام التشغيل:** Windows 10+, macOS 10.14+, Linux (أي توزيعة حديثة)

### الموصى به
- **المعالج:** 2 GHz أو أعلى
- **الذاكرة:** 1 GB RAM
- **المساحة:** 100 MB مساحة حرة
- **الطرفية:** طرفية تدعم الألوان (لتجربة أفضل)

## الدعم

للحصول على المساعدة في التثبيت:
- **البريد الإلكتروني:** eng7mi@gmail.com
- **GitHub Issues:** https://github.com/Alqudimi/GitHydra/issues
- **المستودع:** https://github.com/Alqudimi/GitHydra

## المطور

**الاسم:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**GitHub:** https://github.com/Alqudimi/GitHydra

</div>
