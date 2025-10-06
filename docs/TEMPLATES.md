دليل استخدام نظام القوالب - GitHydra Templates

<div dir="rtl">

نظرة عامة

نظام إدارة القوالب في GitHydra يتيح لك حفظ وإنشاء هياكل المشاريع مسبقة التجهيز. يمكنك حفظ أي مشروع كقالب وإعادة استخدامه لاحقاً، مما يوفر الوقت ويضمن الاتساق بين المشاريع.

المطور

الاسم: عبدالعزيز القديمي
البريد الإلكتروني: eng7mi@gmail.com
المستودع: https://github.com/Alqudimi/GitHydra

المميزات الرئيسية

📁 حفظ هياكل المشاريع

· حفظ أي مجلد كمقالب قابلة لإعادة الاستخدام
· تخزين الهيكل الكامل للمجلدات والملفات
· الحفاظ على محتوى جميع الملفات

🔄 إعادة إنشاء المشاريع

· إنشاء مشاريع جديدة من القوالب المحفوظة
· إعادة إنتاج الهيكل الكامل بدقة
· الحفاظ على أذونات الملفات والمجلدات

📊 التنظيم المتقدم

· تنظيم القوالب في فئات
· البحث والتصفية السهلة
· إحصائيات مفصلة عن كل قالب

🔄 الاستيراد والتصدير

· مشاركة القوالب مع الفريق
· نسخ احتياطي للقوالب
· استيراد قوالب من مصادر خارجية

التثبيت والإعداد

المتطلبات الإضافية

```bash
# تأكد من تثبيت tqdm
pip install tqdm
```

التحديث التلقائي

يتم تحديث GitHydra تلقائياً لدعم نظام القوالب. لا حاجة لإعداد إضافي.

الاستخدام

الوضع التفاعلي (موصى به)

الوصول لنظام القوالب

```bash
githydra interactive
```

ثم اختر الخيار H لإدارة القوالب.

القائمة التفاعلية للقوالب

```
📁 Template Management
1. 📋 List templates        # عرض القوالب المتاحة
2. ➕ Add template          # إضافة قالب جديد
3. 🗑️ Remove template       # حذف قالب
4. 🚀 Create from template  # إنشاء مشروع من قالب
5. 📤 Export templates      # تصدير القوالب
6. 📥 Import templates      # استيراد القوالب
```

وضع سطر الأوامر

عرض القوالب المتاحة

```bash
githydra template list
```

المعلومات المعروضة:

· 📂 الفئة - التصنيف التنظيمي
· 📝 اسم القالب - المعرف الفريد
· 📊 عدد الملفات - إجمالي الملفات في القالب
· 🌳 الهيكل - وجود مخطط الهيكل

إضافة قالب جديد

```bash
# الطريقة التفاعلية
githydra template add

# الطريقة المباشرة
githydra template add --path /مسار/المشروع --category python --name مشروع-جديد
```

الخيارات:

· --path, -p - مسار المجلد المراد حفظه كقالب
· --category, -c - فئة القالب (python, web, mobile, etc.)
· --name, -n - اسم القالب

مثال عملي:

```bash
# حفظ مشروع Flask كقالب
githydra template add --path ~/projects/flask-app --category web --name flask-starter

# حفظ مشروع React كقالب
githydra template add --path ./react-project --category frontend --name react-template
```

إنشاء مشروع من قالب

```bash
# الطريقة التفاعلية
githydra template create

# الطريقة المباشرة
githydra template create --category web --name flask-starter --output ./مشروعي-الجديد
```

الخيارات:

· --category, -c - فئة القالب
· --name, -n - اسم القالب
· --output, -o - مجلد الإخراج (اختياري)

مثال عملي:

```bash
# إنشاء مشروع من قالب Flask
githydra template create --category web --name flask-starter --output ./my-new-app

# إنشاء مشروع في المجلد الحالي
githydra template create --category frontend --name react-template
```

حذف قالب

```bash
# الطريقة التفاعلية
githydra template remove

# الطريقة المباشرة
githydra template remove --category web --name flask-starter
```

مثال عملي:

```bash
# حذف قالب قديم
githydra template remove --category python --name old-project
```

تصدير القوالب

```bash
# تصدير لمسار محدد
githydra template export --output ./نسخة-احتياطية-لقوالب.json

# تصدير للمسار الافتراضي
githydra template export
```

استيراد القوالب

```bash
# استيراد من ملف
githydra template import --input ./قوالب-مستوردة.json

# استيراد تفاعلي
githydra template import
```

أمثلة عملية

مثال 1: إنشاء مكتبة قوالب تطوير ويب

```bash
# إضافة قالب Flask أساسي
githydra template add --category web --name flask-basic --path ~/templates/flask-basic

# إضافة قالب Flask مع قاعدة بيانات
githydra template add --category web --name flask-database --path ~/templates/flask-db

# إضافة قالب React
githydra template add --category frontend --name react-starter --path ~/templates/react-app

# عرض جميع القوالب
githydra template list

# إنشاء مشروع جديد من قالب Flask
githydra template create --category web --name flask-basic --output ./مشروع-ويب-جديد
```

مثال 2: إدارة قوالب الفريق

```bash
# تصدير قوالب الفريق
githydra template export --output ./فريق-قوالب-التطوير.json

# مشاركة الملف مع أعضاء الفريق
# كل عضو يستورد القوالب
githydra template import --input ./فريق-قوالب-التطوير.json

# الآن الجميع لديه نفس القوالب
githydra template list
```

مثال 3: سير عمل تطوير سريع

```bash
# 1. تطوير مشروع نموذجي مرة واحدة
# 2. حفظه كقالب
githydra template add --category api --name fastapi-backend --path ~/projects/backend-template

# 3. عندما تحتاج مشروع جديد
githydra template create --category api --name fastapi-backend --output ./مشروع-العملاء-الجديد

# 4. البدء في التطوير مباشرة!
```

هيكل التخزين

موقع ملف القوالب

```
~/.githydra/
├── templates.json          # قاعدة بيانات القوالب
├── config.yaml            # إعدادات GitHydra
├── aliases.yaml           # الأوامر المختصرة
└── logs/                  # سجلات العمليات
```

تنسيق ملف القوالب (JSON)

```json
{
  "web": {
    "flask-starter": {
      "structure": "مخطط الهيكل...",
      "files": {
        "app.py": "محتوى ملف app.py...",
        "requirements.txt": "محتوى المتطلبات...",
        "templates/index.html": "محتوى HTML...",
        "static/css/style.css": "محتوى CSS..."
      }
    }
  },
  "frontend": {
    "react-template": {
      "structure": "مخطط الهيكل...",
      "files": {
        "package.json": "محتوى package.json...",
        "src/App.js": "محتوى App.js...",
        "public/index.html": "محتوى index.html..."
      }
    }
  }
}
```

أفضل الممارسات

📁 تنظيم القوالب

استخدام فئات واضحة:

```
web/           - تطبيقات الويب
mobile/        - تطبيقات الموبايل  
api/           - واجهات برمجة التطبيقات
cli/           - أدوات سطر الأوامر
library/       - المكتبات
database/      - قواعد البيانات
```

تسمية موحدة:

· استخدام أسماء وصفيّة
· إضافة إصدارات إذا لزم الأمر
· تجنب المسافات، استخدام الشرطات

💾 إدارة القوالب

النسخ الاحتياطي الدوري:

```bash
# نسخ احتياطي أسبوعي
githydra template export --output ~/backups/templates-$(date +%Y-%m-%d).json
```

تنظيف القوالب القديمة:

```bash
# مراجعة دورية وإزالة غير المستخدم
githydra template list
githydra template remove --category old-category --name outdated-template
```

🔄 التعاون مع الفريق

مشاركة القوالب الأساسية:

```bash
# قائد الفريق يصدر القوالب
githydra template export --output ./team-templates.json

# أعضاء الفريق يستوردونها
githydra template import --input ./team-templates.json
```

تحديث القوالب المشتركة:

```bash
# عند تحسين قالب، يصدره القائد من جديد
# الأعضاء يستوردون النسخة المحدثة
```

التكامل مع الميزات الأخرى

مع إدارة المشاريع

```bash
# إنشاء مشروع من قالب
githydra template create --category web --name company-standard --output ./مشروع-عميل-جديد

# ثم إدارة المهام
githydra project init
githydra project issue-create --title "تطوير الواجهة الرئيسية"
```

مع التحكم بالإصدارات

```bash
# إنشاء المشروع من القالب
githydra template create --category python --name data-analysis --output ./تحليل-البيانات

# البدء فوراً في استخدام Git
cd ./تحليل-البيانات
githydra init
githydra stage add --all
githydra commit -m "الهيكل الأولي من القالب"
```

مع السحابة

```bash
# إنشاء مشروع من قالب محلي
githydra template create --category web --name standard-app --output ./تطبيق-سحابي

# رفعه مباشرة إلى GitHub
githydra cloud connect-github
githydra remote add origin https://github.com/user/repo.git
githydra sync push
```

استكشاف الأخطاء

خطأ في استيراد القالب

```
Error: Failed to import template
```

الحل:

· التحقق من صحة تنسيق ملف JSON
· التأكد من صلاحيات القراءة
· فحص سجلات النظام ~/.githydra/logs/

فشل في إنشاء المشروع

```
Error: Output directory not empty
```

الحل:

· استخدام مجلد مختلف للإخراج
· حذف المحتويات يدوياً
· استخدام الخيار --force (إذا متوفر)

قالب غير موجود

```
Error: Template not found
```

الحل:

· التحقق من اسم القالب والفئة githydra template list
· التأكد من تهجئة الأسماء بشكل صحيح
· استيراد القالب إذا كان مفقوداً

الأوامر السريعة

الأمر الوصف
githydra template list عرض جميع القوالب
githydra template add إضافة قالب جديد
githydra template create إنشاء مشروع من قالب
githydra template remove حذف قالب
githydra template export تصدير القوالب
githydra template import استيراد القوالب

نصائح متقدمة

إنشاء قوالب ذكية

· تضمين ملفات التكوين الشائعة
· إضافة تعليمات التشغيل في README
· تضمين ملفات البيئة الافتراضية

إصدارات القوالب

```
web/
  ├── flask-basic-v1
  ├── flask-basic-v2
  └── flask-basic-v3
```

أتمتة سير العمل

```bash
# دمج مع scripts للأتمتة
#!/bin/bash
# create-new-project.sh
githydra template create --category web --name standard-app --output $1
cd $1
githydra init
githydra stage add --all
githydra commit -m "Initial commit from template"
```

الدعم والمساعدة

للحصول على المساعدة في نظام القوالب:

```bash
# عرض المساعدة العامة
githydra template --help

# مساعدة أمر محدد
githydra template add --help

# البحث في السجلات
tail -f ~/.githydra/logs/githydra_*.log
```

البريد الإلكتروني: eng7mi@gmail.com
المستودع: https://github.com/Alqudimi/GitHydra/issues

---

تم التطوير بواسطة: Abdulaziz Alqudimi
الإصدار: 3.1.0
تاريخ الإضافة: أكتوبر 2024

</div>

English Documentation

Template Management System - GitHydra Templates

Overview

GitHydra's Template Management System allows you to save and create pre-configured project structures. You can save any project as a template and reuse it later, saving time and ensuring consistency across projects.

Key Features

📁 Save Project Structures

· Save any folder as reusable templates
· Store complete folder and file structure
· Preserve content of all files

🔄 Recreate Projects

· Create new projects from saved templates
· Reproduce complete structure accurately
· Maintain file and folder permissions

📊 Advanced Organization

· Organize templates in categories
· Easy search and filtering
· Detailed statistics for each template

🔄 Import/Export

· Share templates with team
· Backup templates
· Import templates from external sources

Quick Start

Interactive Mode (Recommended)

```bash
githydra interactive
# Then select H for Template Management
```

Command Line Mode

```bash
# List all templates
githydra template list

# Add a new template
githydra template add --path /project/path --category web --name my-template

# Create project from template
githydra template create --category web --name my-template --output ./new-project

# Remove a template
githydra template remove --category web --name my-template

# Export templates
githydra template export --output ./backup.json

# Import templates
githydra template import --input ./templates.json
```

Examples

Web Development Templates

```bash
# Add Flask template
githydra template add --category web --name flask-app --path ~/projects/flask-template

# Add React template
githydra template add --category frontend --name react-app --path ~/projects/react-template

# Create new project
githydra template create --category web --name flask-app --output ./client-project
```

Team Collaboration

```bash
# Export team templates
githydra template export --output ./team-templates.json

# Import shared templates
githydra template import --input ./team-templates.json
```

Best Practices

Organization

· Use clear categories (web, mobile, api, cli, library, database)
· Use descriptive names
· Avoid spaces, use hyphens

Maintenance

```bash
# Weekly backup
githydra template export --output ~/backups/templates-$(date +%Y-%m-%d).json

# Regular cleanup
githydra template list
githydra template remove --category old-category --name outdated-template
```

Troubleshooting

Common Issues

· Import errors: Check JSON file format and permissions
· Template not found: Verify template name and category spelling
· Output directory not empty: Use different directory or clear contents

Getting Help

```bash
# General help
githydra template --help

# Command-specific help
githydra template add --help

# Check logs
tail -f ~/.githydra/logs/githydra_*.log
```

Developer: Abdulaziz Alqudimi
Email: eng7mi@gmail.com
Repository: https://github.com/Alqudimi/GitHydra

---

Version: 3.1.0
Release Date: October 2024