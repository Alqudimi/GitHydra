# GitHydra - أداة CLI شاملة لأتمتة Git

<div dir="rtl">

## نظرة عامة

GitHydra هي أداة قوية مبنية على Python توفر واجهة جميلة وبديهية لإدارة جميع عمليات Git. تم بناؤها باستخدام Rich لواجهة مستخدم رائعة في الطرفية، وClick لإطار عمل CLI قوي، وGitPython للتكامل مع Git.

## المطور

**الاسم:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra

## المميزات الرئيسية

### 1️⃣ عمليات المستودع
- تهيئة المستودعات
- عرض الحالة التفصيلية
- الاستنساخ مع تتبع التقدم
- إنشاء الأرشيف
- تنظيف الملفات غير المتعقبة

### 2️⃣ الملفات والتجهيز
- منطقة تجهيز تفاعلية
- اختيار ذكي للملفات
- إدارة التغييرات المُجهزة/غير المُجهزة
- عرض الفروقات
- معلومات المؤلف للملفات

### 3️⃣ الالتزامات والتاريخ
- إنشاء التزامات جميلة
- تعديل الالتزامات السابقة
- عرض سجل الالتزامات (مع خيار الرسم البياني)
- عرض سجلات المراجع
- إضافة ملاحظات للالتزامات

### 4️⃣ الفروع
- إنشاء وحذف وإعادة تسمية الفروع
- التبديل بين الفروع بسلاسة
- دمج الفروع
- مقارنة الفروع
- تتبع الفروع البعيدة

### 5️⃣ البعيد والمزامنة
- إدارة المستودعات البعيدة
- عمليات الدفع/السحب/الجلب
- استراتيجيات المزامنة الذكية
- مقارنة مع الفروع البعيدة

### 6️⃣ العمليات المتقدمة
- إدارة المخبأ (Stash)
- إنشاء الوسوم (Tags)
- إعادة التعيين والتراجع والانتقاء
- عارض فروقات محسّن
- إعادة الأساس التفاعلية

### 7️⃣ الوحدات الفرعية وأشجار العمل
- **الوحدات الفرعية:** إضافة، تهيئة، تحديث، عرض الحالة، مزامنة، تنفيذ، إلغاء التهيئة
- **أشجار العمل:** إنشاء أشجار عمل متعددة، عرض القائمة، إزالة، تقليم، قفل/إلغاء القفل، نقل

### 8️⃣ التصحيح والبحث
- **Bisect:** بحث ثنائي للعثور على الأخطاء
- **Blame:** معلومات المؤلف سطراً بسطر مع الإحصائيات
- **Reflog:** عرض وإدارة سجلات المراجع

### 9️⃣ التصحيحات والحزم
- **التصحيحات:** إنشاء وتطبيق وتنسيق التصحيحات للبريد الإلكتروني
- **الحزم:** نقل المستودعات عبر ملفات الحزم

### 🅰️ النزاعات والدمج
- عرض الملفات المتعارضة
- قبول استراتيجيات "ours/theirs"
- تشغيل أدوات الدمج
- إحباط العمليات بأمان

### 🅱️ الإحصائيات والتحليل
- نظرة عامة على المستودع
- إحصائيات المساهمين
- تحليل النشاط
- إحصائيات الملفات
- توزيع اللغات البرمجية

### ©️ الصيانة والإصلاح
- فحص سلامة المستودع
- تحسين مع جمع القمامة
- تقليم الكائنات غير القابلة للوصول
- إصلاح الفهرس
- عرض معلومات المستودع

### 🅳 التكوين
- إدارة تكوين Git
- إدارة تكوين GitHydra
- الأوامر المختصرة (Aliases)

## التثبيت

### عبر pip
```bash
pip install -e .
```

### باستخدام سكريبتات التثبيت
```bash
# Linux/Mac
./install.sh

# Windows
install.bat
```

## الاستخدام

### الوضع التفاعلي (موصى به للمبتدئين)
```bash
githydra interactive
```

### وضع سطر الأوامر
```bash
githydra --help
githydra init [path]
githydra status
githydra stage add --interactive
githydra commit -m "رسالة الالتزام"
githydra branch list
githydra log --graph
githydra sync push
```

## الأوامر الأساسية

### عمليات المستودع
```bash
githydra init                     # تهيئة مستودع جديد
githydra status                   # عرض حالة المستودع
githydra sync clone <url>         # استنساخ مستودع
```

### إدارة الملفات
```bash
githydra stage add --interactive  # تجهيز ملفات (تفاعلي)
githydra stage add --all          # تجهيز جميع الملفات
githydra stage remove --all       # إلغاء تجهيز الملفات
githydra diff                     # عرض الفروقات
```

### الالتزامات
```bash
githydra commit -m "رسالة"        # إنشاء التزام
githydra commit --amend           # تعديل آخر التزام
githydra log                      # عرض سجل الالتزامات
githydra log --graph              # عرض الرسم البياني
```

### الفروع
```bash
githydra branch list              # عرض الفروع
githydra branch create <name>     # إنشاء فرع
githydra branch switch <name>     # التبديل للفرع
githydra branch delete <name>     # حذف فرع
githydra branch merge <name>      # دمج فرع
```

### المزامنة
```bash
githydra remote add <name> <url>  # إضافة مستودع بعيد
githydra sync push                # دفع التغييرات
githydra sync pull                # سحب التغييرات
githydra sync fetch               # جلب التحديثات
```

### العمليات المتقدمة
```bash
githydra stash save -m "رسالة"    # حفظ التغييرات مؤقتاً
githydra stash list               # عرض قائمة المخبأ
githydra stash apply              # تطبيق المخبأ
githydra tag create v1.0          # إنشاء وسم
githydra reset --soft HEAD~1      # إعادة تعيين ناعمة
```

### الوحدات الفرعية
```bash
githydra submodule add <url>      # إضافة وحدة فرعية
githydra submodule update         # تحديث الوحدات الفرعية
githydra submodule status         # حالة الوحدات الفرعية
```

### أشجار العمل
```bash
githydra worktree add <path>      # إضافة شجرة عمل
githydra worktree list            # عرض أشجار العمل
githydra worktree remove <path>   # إزالة شجرة عمل
```

### التصحيح
```bash
githydra bisect start             # بدء bisect
githydra bisect good              # تحديد التزام جيد
githydra bisect bad               # تحديد التزام سيء
githydra bisect reset             # إنهاء bisect
githydra blame <file>             # عرض معلومات المؤلف
```

### الإحصائيات
```bash
githydra stats overview           # نظرة عامة على المستودع
githydra stats contributors       # إحصائيات المساهمين
githydra stats activity           # تحليل النشاط
githydra stats files              # إحصائيات الملفات
githydra stats languages          # توزيع اللغات
```

## المتطلبات

- Python 3.11 أو أحدث
- rich - تنسيق الطرفية والواجهة
- click - إطار عمل CLI
- gitpython - واجهة مستودع Git
- questionary - مطالبات تفاعلية
- pyyaml - إدارة التكوين
- colorama - إخراج ملون عبر المنصات

## التكوين

يخزن GitHydra التكوين والسجلات في `~/.githydra/`:
- `config.yaml` - تكوين المستخدم
- `aliases.yaml` - الأوامر المختصرة
- `logs/` - سجلات العمليات حسب التاريخ

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT.

## الدعم

للحصول على الدعم، يرجى التواصل مع:
- **البريد الإلكتروني:** eng7mi@gmail.com
- **GitHub:** https://github.com/Alqudimi/GitHydra

</div>
