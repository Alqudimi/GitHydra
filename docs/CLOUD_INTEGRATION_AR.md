# التكامل السحابي - Cloud Integration

## نظرة عامة

يوفر GitHydra تكاملاً قوياً مع خدمات السحابة مثل GitHub، مما يتيح لك إدارة المستودعات السحابية، المزامنة، النسخ الاحتياطي، وتتبع المشاكل مباشرة من سطر الأوامر.

## المميزات الرئيسية

### 🔐 المصادقة مع GitHub

قم بربط حسابك على GitHub بشكل آمن باستخدام رمز الوصول الشخصي (Personal Access Token).

```bash
githydra cloud connect-github
```

أو باستخدام الرمز مباشرة:

```bash
githydra cloud connect-github --token YOUR_TOKEN
```

**كيفية الحصول على رمز GitHub:**
1. انتقل إلى GitHub → Settings → Developer settings → Personal access tokens
2. اختر "Generate new token (classic)"
3. حدد الصلاحيات المطلوبة: `repo`, `read:user`, `read:org`
4. انسخ الرمز واستخدمه مع GitHydra

**التخزين الآمن:**
يتم حفظ الرمز بشكل آمن في `~/.githydra/github_token`

---

### 📚 إدارة المستودعات

#### عرض قائمة المستودعات الخاصة بك

```bash
githydra cloud repos
```

عرض أول 20 مستودع:
```bash
githydra cloud repos --limit 20
```

**المعلومات المعروضة:**
- 📦 اسم المستودع
- 🌐 نوع المستودع (عام/خاص) واللغة
- ⭐ عدد النجوم
- 🔀 عدد الـ Forks
- 📅 تاريخ آخر تحديث

---

### 🔄 المزامنة مع GitHub

قم بمزامنة المستودع المحلي مع مستودع على GitHub:

```bash
githydra cloud sync --repo owner/repo-name
```

أو بدون تحديد المستودع (سيطلب منك إدخاله):
```bash
githydra cloud sync
```

**ما تفعله المزامنة:**
1. تسحب آخر التغييرات من المستودع البعيد
2. تدمج التغييرات مع الفرع الحالي
3. تعرض ملخصاً للتحديثات

---

### 💾 النسخ الاحتياطي للمستودع

أنشئ نسخة احتياطية كاملة من المستودع بما في ذلك جميع الملفات وسجل Git:

```bash
githydra cloud backup
```

تحديد مجلد الحفظ:
```bash
githydra cloud backup --output /path/to/backup
```

**محتويات النسخة الاحتياطية:**
- ✅ مجلد `.git` الكامل مع جميع السجلات
- ✅ جميع الملفات المتتبعة وغير المتتبعة
- ✅ حماية من التكرار اللانهائي (النسخ الاحتياطي لا ينسخ نفسه)

**معلومات النسخة الاحتياطية:**
- 📍 موقع الحفظ
- 📦 اسم المستودع
- 🌿 اسم الفرع
- 📝 عدد الـ Commits
- 💾 حجم النسخة الاحتياطية

---

### 🐛 تتبع المشاكل (Issues)

عرض المشاكل من أي مستودع على GitHub:

```bash
githydra cloud issues --repo owner/repo-name
```

عرض المشاكل المغلقة:
```bash
githydra cloud issues --repo owner/repo-name --state closed
```

عرض جميع المشاكل:
```bash
githydra cloud issues --repo owner/repo-name --state all
```

**المعلومات المعروضة:**
- #️⃣ رقم المشكلة
- 📝 عنوان المشكلة
- 🔴 الحالة (مفتوحة/مغلقة)
- 👤 المؤلف
- 💬 عدد التعليقات

---

### 🏷️ الإصدارات (Releases)

عرض إصدارات أي مستودع:

```bash
githydra cloud releases --repo owner/repo-name
```

**المعلومات المعروضة:**
- 🏷️ اسم الوسم (Tag)
- 📄 عنوان الإصدار
- 🔖 نوع الإصدار (Pre-release أو عادي)
- 📦 عدد الملفات المرفقة
- 📅 تاريخ النشر

---

## أمثلة عملية

### مثال 1: الاتصال ومزامنة مستودع

```bash
# الاتصال بـ GitHub
githydra cloud connect-github

# عرض المستودعات
githydra cloud repos --limit 10

# مزامنة مع مستودع معين
githydra cloud sync --repo myusername/myproject
```

### مثال 2: إنشاء نسخة احتياطية

```bash
# نسخ احتياطي في المجلد الافتراضي
githydra cloud backup

# نسخ احتياطي في مجلد محدد
githydra cloud backup --output ~/backups/myproject_backup
```

### مثال 3: تتبع المشاكل والإصدارات

```bash
# عرض المشاكل المفتوحة
githydra cloud issues --repo facebook/react --state open

# عرض آخر الإصدارات
githydra cloud releases --repo nodejs/node
```

---

## نصائح وأفضل الممارسات

### 🔒 الأمان
- **لا تشارك رمز GitHub** مع أي شخص
- استخدم رموز ذات صلاحيات محددة فقط
- قم بتحديث الرمز بشكل دوري

### 💡 الاستخدام الأمثل
- **النسخ الاحتياطي الدوري**: قم بعمل نسخ احتياطية منتظمة
- **المزامنة قبل العمل**: دائماً زامن مع السحابة قبل بدء العمل
- **تتبع المشاكل**: استخدم تتبع المشاكل لمتابعة المشاريع الكبيرة

### ⚙️ التكوين
موقع ملفات التكوين:
- رمز GitHub: `~/.githydra/github_token`
- ملفات السجل: `~/.githydra/logs/`

---

## استكشاف الأخطاء

### خطأ في المصادقة
```
Error: GitHub authentication failed
```
**الحل**: تأكد من صحة الرمز وأنه يحتوي على الصلاحيات المطلوبة

### فشل المزامنة
```
Error: Failed to sync repository
```
**الحل**: 
- تأكد من وجود اتصال بالإنترنت
- تحقق من صحة اسم المستودع (owner/repo)
- تأكد من وجود صلاحيات الوصول للمستودع

### مشاكل النسخ الاحتياطي
```
Error: Failed to create backup
```
**الحل**:
- تأكد من وجود مساحة كافية
- تحقق من صلاحيات الكتابة في مجلد الحفظ
- تأكد من أنك في مجلد مستودع Git صحيح

---

## الأوامر السريعة

| الأمر | الوصف |
|-------|--------|
| `githydra cloud connect-github` | الاتصال بـ GitHub |
| `githydra cloud repos` | عرض المستودعات |
| `githydra cloud sync` | المزامنة مع GitHub |
| `githydra cloud backup` | نسخ احتياطي للمستودع |
| `githydra cloud issues` | عرض المشاكل |
| `githydra cloud releases` | عرض الإصدارات |

---

## التكامل مع الميزات الأخرى

يعمل التكامل السحابي بسلاسة مع:
- 📊 **إدارة المشاريع**: يمكن ربط المشاكل المحلية مع GitHub
- ⭐ **التعاون الجماعي**: تتبع المساهمات والـ Pull Requests
- 🔧 **الأوامر الأساسية**: جميع أوامر Git الأساسية تعمل مع المستودعات السحابية

---

**تم التطوير بواسطة:** Abdulaziz Alqudimi  
**الإصدار:** 3.0.0  
**المزيد من المساعدة:** استخدم `githydra cloud --help` لعرض جميع الخيارات
