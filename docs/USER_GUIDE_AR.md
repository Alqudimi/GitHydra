# دليل المستخدم - GitHydra

<div dir="rtl">

## مقدمة

GitHydra هي أداة سطر أوامر شاملة تجعل استخدام Git أسهل وأكثر إنتاجية. توفر الأداة واجهة جميلة وبديهية لجميع عمليات Git.

## البدء السريع

### تشغيل الوضع التفاعلي
```bash
githydra interactive
```

الوضع التفاعلي هو أسهل طريقة لاستخدام GitHydra، حيث يوفر قوائم منظمة لجميع الأوامر المتاحة.

## الأوامر الأساسية

### 1. عمليات المستودع

#### تهيئة مستودع جديد
```bash
githydra init
githydra init /path/to/directory
```

#### عرض حالة المستودع
```bash
githydra status
```

#### استنساخ مستودع
```bash
githydra sync clone <url>
githydra sync clone https://github.com/Alqudimi/GitHydra.git
```

#### إنشاء أرشيف
```bash
githydra archive create
githydra archive create --format zip
githydra archive create --format tar.gz
```

#### تنظيف الملفات غير المتعقبة
```bash
githydra clean
githydra clean --dry-run    # معاينة فقط
githydra clean --force      # حذف فعلي
```

### 2. إدارة الملفات والتجهيز

#### تجهيز الملفات (تفاعلي)
```bash
githydra stage add --interactive
```

#### تجهيز جميع الملفات
```bash
githydra stage add --all
```

#### تجهيز ملفات محددة
```bash
githydra stage add file1.py file2.py
```

#### إلغاء تجهيز الملفات
```bash
githydra stage remove --all
githydra stage remove file1.py
```

#### عرض الفروقات
```bash
githydra diff                # فروقات غير مُجهزة
githydra stage diff          # فروقات مُجهزة
githydra diff --cached       # فروقات مُجهزة (بديل)
```

#### عرض معلومات المؤلف
```bash
githydra blame <file>
githydra blame src/main.py
```

### 3. الالتزامات والتاريخ

#### إنشاء التزام
```bash
githydra commit -m "رسالة الالتزام"
githydra commit -m "إضافة ميزة جديدة" -m "وصف تفصيلي"
```

#### تعديل آخر التزام
```bash
githydra commit --amend
githydra commit --amend -m "رسالة محدثة"
```

#### عرض سجل الالتزامات
```bash
githydra log
githydra log --graph        # عرض رسم بياني
githydra log -n 10          # آخر 10 التزامات
githydra log --author="الاسم"
```

#### عرض سجل المراجع (Reflog)
```bash
githydra reflog show
githydra reflog show --all
```

#### إضافة ملاحظات للالتزامات
```bash
githydra notes add
githydra notes show <commit>
githydra notes list
githydra notes remove <commit>
```

### 4. إدارة الفروع

#### عرض الفروع
```bash
githydra branch list
githydra branch list --all       # جميع الفروع
githydra branch list --remote    # الفروع البعيدة فقط
```

#### إنشاء فرع جديد
```bash
githydra branch create <branch-name>
githydra branch create feature/new-feature
```

#### التبديل بين الفروع
```bash
githydra branch switch <branch-name>
githydra branch switch main
```

#### حذف فرع
```bash
githydra branch delete <branch-name>
githydra branch delete --force <branch-name>
```

#### إعادة تسمية فرع
```bash
githydra branch rename <new-name>
```

#### دمج فرع
```bash
githydra branch merge <branch-name>
githydra branch merge feature/new-feature
```

#### مقارنة الفروع
```bash
githydra compare branches <branch1> <branch2>
githydra compare branches main develop
```

### 5. المستودعات البعيدة والمزامنة

#### عرض المستودعات البعيدة
```bash
githydra remote list
githydra remote list -v         # مع التفاصيل
```

#### إضافة مستودع بعيد
```bash
githydra remote add <name> <url>
githydra remote add origin https://github.com/user/repo.git
```

#### إزالة مستودع بعيد
```bash
githydra remote remove <name>
```

#### دفع التغييرات
```bash
githydra sync push
githydra sync push origin main
githydra sync push --force      # دفع إجباري (احذر!)
```

#### سحب التغييرات
```bash
githydra sync pull
githydra sync pull origin main
githydra sync pull --rebase     # مع إعادة الأساس
```

#### جلب التحديثات
```bash
githydra sync fetch
githydra sync fetch --all       # من جميع المستودعات
```

#### مقارنة مع البعيد
```bash
githydra compare with-remote
githydra compare with-remote origin/main
```

### 6. العمليات المتقدمة

#### إدارة المخبأ (Stash)
```bash
githydra stash save -m "عمل قيد التنفيذ"
githydra stash list
githydra stash apply            # تطبيق آخر مخبأ
githydra stash apply stash@{0}  # تطبيق مخبأ محدد
githydra stash pop              # تطبيق وحذف
githydra stash drop             # حذف مخبأ
githydra stash clear            # حذف جميع المخابئ
```

#### إدارة الوسوم (Tags)
```bash
githydra tag create v1.0.0
githydra tag create v1.0.0 -m "إصدار 1.0"
githydra tag list
githydra tag delete v1.0.0
githydra tag push v1.0.0        # دفع وسم للبعيد
```

#### إعادة التعيين (Reset)
```bash
githydra reset --soft HEAD~1    # إلغاء آخر التزام (حفظ التغييرات)
githydra reset --mixed HEAD~1   # إلغاء التزام + تجهيز
githydra reset --hard HEAD~1    # إلغاء كل شيء (احذر!)
```

#### التراجع (Revert)
```bash
githydra revert <commit-hash>
```

#### الانتقاء (Cherry-pick)
```bash
githydra cherry-pick <commit-hash>
```

#### إعادة الأساس التفاعلية
```bash
githydra rebase start <branch>
githydra rebase start --interactive HEAD~3
githydra rebase continue
githydra rebase skip
githydra rebase abort
```

### 7. الوحدات الفرعية (Submodules)

#### إضافة وحدة فرعية
```bash
githydra submodule add <url> <path>
githydra submodule add https://github.com/user/lib.git libs/mylib
```

#### تهيئة الوحدات الفرعية
```bash
githydra submodule init
```

#### تحديث الوحدات الفرعية
```bash
githydra submodule update
githydra submodule update --remote    # تحديث لأحدث إصدار
```

#### عرض حالة الوحدات الفرعية
```bash
githydra submodule status
```

#### مزامنة الوحدات الفرعية
```bash
githydra submodule sync
```

#### تنفيذ أمر على جميع الوحدات
```bash
githydra submodule foreach <command>
githydra submodule foreach git pull
```

#### إلغاء تهيئة وحدة فرعية
```bash
githydra submodule deinit <path>
```

### 8. أشجار العمل (Worktrees)

#### إضافة شجرة عمل
```bash
githydra worktree add <path> <branch>
githydra worktree add ../project-feature feature/new-feature
```

#### عرض أشجار العمل
```bash
githydra worktree list
```

#### إزالة شجرة عمل
```bash
githydra worktree remove <path>
```

#### تقليم أشجار العمل
```bash
githydra worktree prune
```

#### قفل شجرة عمل
```bash
githydra worktree lock <path>
githydra worktree unlock <path>
```

#### نقل شجرة عمل
```bash
githydra worktree move <source> <destination>
```

### 9. التصحيح والبحث

#### استخدام Bisect للعثور على الأخطاء
```bash
githydra bisect start
githydra bisect bad              # الالتزام الحالي سيء
githydra bisect good <commit>    # التزام جيد معروف
# Git سيختار التزامات للاختبار
githydra bisect good             # بعد الاختبار
githydra bisect bad              # بعد الاختبار
githydra bisect reset            # الانتهاء
```

#### عرض معلومات المؤلف (Blame)
```bash
githydra blame <file>
githydra blame -L 10,20 <file>   # أسطر محددة
```

#### إدارة Reflog
```bash
githydra reflog show
githydra reflog expire --expire=30.days
githydra reflog delete <ref@{n}>
```

### 10. التصحيحات والحزم

#### إنشاء تصحيح
```bash
githydra patch create
githydra patch create --output-dir patches/
```

#### تطبيق تصحيح
```bash
githydra patch apply <patch-file>
```

#### تنسيق تصحيح للبريد
```bash
githydra patch format-patch HEAD~3
```

#### إنشاء حزمة
```bash
githydra bundle create <file> <refs>
githydra bundle create repo.bundle --all
```

#### التحقق من حزمة
```bash
githydra bundle verify <file>
```

#### فك حزمة
```bash
githydra bundle unbundle <file>
```

### 11. حل النزاعات

#### عرض الملفات المتعارضة
```bash
githydra conflicts list
```

#### عرض تفاصيل النزاع
```bash
githydra conflicts show <file>
```

#### قبول نسخة معينة
```bash
githydra conflicts accept-ours <file>
githydra conflicts accept-theirs <file>
```

#### إحباط عملية الدمج
```bash
githydra conflicts abort
```

#### تشغيل أداة الدمج
```bash
githydra conflicts mergetool
```

### 12. الإحصائيات والتحليل

#### نظرة عامة على المستودع
```bash
githydra stats overview
```

#### إحصائيات المساهمين
```bash
githydra stats contributors
```

#### تحليل النشاط
```bash
githydra stats activity
githydra stats activity --days 30
```

#### إحصائيات الملفات
```bash
githydra stats files
```

#### توزيع اللغات
```bash
githydra stats languages
```

### 13. الصيانة والإصلاح

#### فحص سلامة المستودع
```bash
githydra repair check
```

#### تحسين المستودع
```bash
githydra repair optimize
```

#### تقليم الكائنات
```bash
githydra repair prune
```

#### إصلاح الفهرس
```bash
githydra repair index
```

#### معلومات المستودع
```bash
githydra repair info
```

### 14. التكوين

#### عرض التكوين
```bash
githydra config list
githydra config get <key>
```

#### تعيين تكوين
```bash
githydra config set <key> <value>
githydra config set user.name "عبدالعزيز القديمي"
githydra config set user.email "eng7mi@gmail.com"
```

#### حذف تكوين
```bash
githydra config unset <key>
```

#### الأوامر المختصرة
```bash
githydra alias list
githydra alias set <name> <command>
githydra alias set st status
githydra alias remove <name>
```

## نصائح وإرشادات

### 1. استخدام الوضع التفاعلي
- أسهل للمبتدئين
- منظم في قوائم واضحة
- يوفر جميع الخيارات المتاحة

### 2. الاستفادة من الألوان
- الأخضر: نجاح
- الأحمر: خطأ أو تحذير
- الأزرق: معلومات
- الأصفر: تنبيه

### 3. قراءة السجلات
- جميع العمليات مسجلة في `~/.githydra/logs/`
- مفيدة لتتبع الأخطاء
- منظمة حسب التاريخ

### 4. استخدام الأوامر المختصرة
```bash
githydra alias set st status
githydra alias set co commit
githydra alias set br branch
```

### 5. التكوين المخصص
- عدّل `~/.githydra/config.yaml` حسب تفضيلاتك
- أضف أوامر مختصرة في `~/.githydra/aliases.yaml`

## أمثلة عملية

### مثال 1: البدء بمشروع جديد
```bash
githydra init my-project
cd my-project
# إنشاء ملفات
githydra stage add --all
githydra commit -m "التزام أولي"
githydra remote add origin <url>
githydra sync push -u origin main
```

### مثال 2: المساهمة في مشروع
```bash
githydra sync clone <url>
cd project
githydra branch create feature/my-feature
# إجراء تعديلات
githydra stage add --interactive
githydra commit -m "إضافة ميزة جديدة"
githydra sync push origin feature/my-feature
```

### مثال 3: حل نزاع دمج
```bash
githydra branch merge feature-branch
# نزاع يحدث
githydra conflicts list
githydra conflicts show <file>
# حل النزاع يدوياً
githydra stage add <file>
githydra commit -m "حل النزاع"
```

## الدعم

للحصول على المساعدة:
- **البريد الإلكتروني:** eng7mi@gmail.com
- **GitHub:** https://github.com/Alqudimi/GitHydra
- **التوثيق:** راجع الملفات في مجلد docs/

## المطور

**الاسم:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra

</div>
