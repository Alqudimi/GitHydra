# التعاون الجماعي - Team Collaboration

## نظرة عامة

يوفر GitHydra أدوات متقدمة للتعاون الجماعي، بما في ذلك تحليل المساهمين، تتبع نشاط الفريق، إدارة Pull Requests، مراجعة الأكواد، وأدلة سير العمل الجماعي.

## المميزات الرئيسية

### ⭐ تحليل المساهمين

#### عرض إحصائيات المساهمين

```bash
githydra team contributors
```

**المعلومات المعروضة:**
- 👤 **اسم المساهم**
- 📧 **البريد الإلكتروني**
- 📝 **عدد الـ Commits**
- ➕ **الأسطر المضافة**
- ➖ **الأسطر المحذوفة**
- 📅 **تاريخ آخر مساهمة**

**التحليل:**
- يتم تحليل آخر 200 commit
- ترتيب المساهمين حسب عدد الـ commits
- إحصائيات مفصلة لكل مساهم
- عرض مرئي جميل في جدول احترافي

---

### 📊 نشاط الفريق

#### عرض نشاط الفريق

```bash
githydra team activity
```

عرض نشاط آخر 60 يوم:
```bash
githydra team activity --days 60
```

**المعلومات المعروضة:**
- 📅 **النشاط اليومي**: عدد الـ commits في كل يوم
- 📈 **رسم بياني نصي**: تمثيل مرئي للنشاط
- 👥 **عدد المساهمين النشطين**
- 📊 **متوسط الـ Commits يومياً**

**الإحصائيات:**
- إجمالي الـ Commits في الفترة
- عدد المساهمين النشطين
- متوسط النشاط اليومي
- مدة التحليل بالأيام

---

### 🔀 إدارة Pull Requests

#### عرض قائمة Pull Requests

```bash
githydra team pr-list --repo owner/repo-name
```

عرض PRs المغلقة:
```bash
githydra team pr-list --repo owner/repo-name --state closed
```

عرض جميع PRs:
```bash
githydra team pr-list --repo owner/repo-name --state all
```

**المعلومات المعروضة:**
- #️⃣ **رقم PR**
- 📝 **العنوان**
- ✅ **الحالة** (مفتوح/مغلق/مدمج)
- 👤 **المؤلف**
- 💬 **عدد التعليقات**
- 📅 **تاريخ الإنشاء**

**حالات Pull Request:**
- ✅ **Merged**: تم الدمج بنجاح
- 🔀 **Open**: مفتوح وفي انتظار المراجعة
- ❌ **Closed**: مغلق بدون دمج

---

### 🔍 مراجعة الفروع (Branch Review)

#### مراجعة التغييرات في فرع

```bash
githydra team review
```

مراجعة فرع محدد:
```bash
githydra team review --branch feature-branch
```

**ما يعرضه التحليل:**

1. **مقارنة الفروع:**
   - الفرق بين الفرع الحالي والفرع المستهدف
   - إحصائيات التغييرات (ملفات، إضافات، حذف)

2. **الـ Commits الجديدة:**
   - قائمة بجميع الـ commits الجديدة في الفرع
   - معلومات كل commit (Hash, Author, Message, Date)

3. **تحليل التغييرات:**
   - عرض تفصيلي للملفات المعدلة
   - إحصائيات التعديلات

---

### 📚 دليل سير العمل الجماعي

#### عرض دليل أفضل الممارسات

```bash
githydra team workflow
```

**يتضمن الدليل:**

**سير العمل الموصى به:**
1. 🌿 إنشاء فرع للميزة الجديدة
2. 📝 عمل commits برسائل واضحة
3. ⬆️ رفع الفرع إلى المستودع البعيد
4. 🔀 إنشاء Pull Request
5. 🔍 مراجعة الكود من قبل الفريق
6. ✅ دمج الفرع إلى الفرع الرئيسي

**أفضل الممارسات:**
- ⭐ كتابة رسائل commit وصفية
- ⭐ مراجعة الكود قبل الدمج
- ⭐ الحفاظ على الفروع محدثة
- ⭐ استخدام أسماء فروع ذات معنى
- ⭐ الاختبار قبل الرفع

---

## أمثلة عملية

### مثال 1: تحليل مساهمات الفريق

```bash
# عرض المساهمين
githydra team contributors

# النتيجة ستظهر:
# - أكثر المساهمين نشاطاً
# - عدد الأسطر المضافة والمحذوفة
# - آخر نشاط لكل مساهم
```

### مثال 2: تتبع نشاط المشروع

```bash
# نشاط آخر 30 يوم (افتراضي)
githydra team activity

# نشاط آخر 90 يوم
githydra team activity --days 90

# النتيجة:
# - رسم بياني للنشاط اليومي
# - إحصائيات الفريق
# - متوسط الإنتاجية
```

### مثال 3: مراجعة Pull Requests

```bash
# عرض PRs المفتوحة في مستودع
githydra team pr-list --repo facebook/react --state open

# عرض جميع PRs
githydra team pr-list --repo nodejs/node --state all
```

### مثال 4: مراجعة فرع قبل الدمج

```bash
# اختيار فرع للمراجعة (سيعرض قائمة)
githydra team review

# أو تحديد الفرع مباشرة
githydra team review --branch feature-new-ui

# النتيجة:
# - التغييرات بين الفروع
# - الـ commits الجديدة
# - ملخص التعديلات
```

---

## سير عمل الفريق الموصى به

### 1. بدء ميزة جديدة

```bash
# إنشاء فرع جديد
githydra branch create feature-user-auth

# التبديل إلى الفرع
githydra branch switch feature-user-auth
```

### 2. العمل والتطوير

```bash
# إضافة الملفات
githydra stage add --all

# عمل commit
githydra commit -m "إضافة نظام تسجيل الدخول"

# رفع إلى المستودع البعيد
githydra sync push
```

### 3. طلب المراجعة

```bash
# عرض التغييرات للمراجعة الذاتية
githydra team review --branch feature-user-auth

# بعد التأكد، افتح PR على GitHub
# (يمكن استخدام GitHub Web أو CLI)
```

### 4. دمج الكود

```bash
# بعد الموافقة، التبديل للفرع الرئيسي
githydra branch switch main

# دمج الفرع
githydra branch merge feature-user-auth
```

---

## التكامل مع GitHub

### متطلبات الاستخدام

لاستخدام ميزات GitHub (PR list):
1. الاتصال بـ GitHub أولاً:
```bash
githydra cloud connect-github
```

2. استخدام ميزات الفريق مع GitHub:
```bash
githydra team pr-list --repo owner/repo
```

### الميزات المتكاملة

- ✅ قراءة Pull Requests من GitHub
- ✅ عرض حالة PRs (مفتوح/مغلق/مدمج)
- ✅ عرض التعليقات والمراجعات
- ✅ تحليل المساهمين من GitHub

---

## قياس أداء الفريق

### مؤشرات الأداء الرئيسية (KPIs)

1. **عدد الـ Commits:**
   - مؤشر على نشاط التطوير
   - يظهر في `team contributors`

2. **تكرار المساهمات:**
   - منتظم = فريق نشط
   - يظهر في `team activity`

3. **سرعة الدمج:**
   - عدد PRs المفتوحة vs المدمجة
   - يظهر في `team pr-list`

4. **توزيع العمل:**
   - توازن المساهمات بين الأعضاء
   - يظهر في `team contributors`

---

## أفضل ممارسات التعاون

### 📝 رسائل Commit

**جيد:**
```bash
git commit -m "إضافة: نظام المصادقة للمستخدمين"
git commit -m "إصلاح: خطأ في تسجيل الدخول (#123)"
git commit -m "تحديث: تحسين أداء قاعدة البيانات"
```

**سيء:**
```bash
git commit -m "تعديلات"
git commit -m "fix"
git commit -m "update code"
```

### 🔍 مراجعة الكود

**قبل المراجعة:**
- ✅ تأكد من عمل الكود
- ✅ قم بتشغيل الاختبارات
- ✅ اكتب رسالة commit واضحة
- ✅ راجع تغييراتك بنفسك أولاً

**أثناء المراجعة:**
- 👀 راجع كل سطر بعناية
- 💬 اكتب تعليقات بناءة
- ✨ اقترح تحسينات
- ⏰ راجع في وقت معقول

### 🚀 إدارة الفروع

**تسمية الفروع:**
```
feature/user-authentication
bugfix/login-error
hotfix/security-patch
enhancement/performance-improvement
```

**نظافة الفروع:**
```bash
# حذف الفروع المدمجة
githydra branch delete old-feature-branch
```

---

## الأوامر السريعة

| الأمر | الوصف |
|-------|--------|
| `githydra team contributors` | عرض المساهمين |
| `githydra team activity` | عرض نشاط الفريق |
| `githydra team pr-list` | عرض Pull Requests |
| `githydra team review` | مراجعة فرع |
| `githydra team workflow` | عرض دليل سير العمل |

---

## استكشاف الأخطاء

### عدم الاتصال بـ GitHub
```
Error: Not connected to GitHub
```
**الحل**: قم بتشغيل `githydra cloud connect-github` أولاً

### لا يوجد مساهمين
```
Info: No contributors found
```
**الحل**: تأكد من أنك في مستودع Git يحتوي على commits

### خطأ في قراءة PRs
```
Error: Failed to list pull requests
```
**الحل**: 
- تحقق من صحة اسم المستودع
- تأكد من صلاحيات الوصول
- تحقق من اتصال الإنترنت

---

## نصائح للفرق الكبيرة

### تنظيم العمل

1. **استخدم المعالم (Milestones)**:
```bash
githydra project milestone-create --title "Sprint 1"
```

2. **وزع المهام**:
```bash
githydra project issue-create --title "مهمة للمطور A"
```

3. **راقب التقدم**:
```bash
githydra project board
githydra team activity
```

### التواصل الفعال

- 💬 استخدم التعليقات في PRs
- 📝 اكتب وصف واضح للمهام
- 🎯 حدد أهداف واضحة
- 📊 راجع الإحصائيات بانتظام

---

## التكامل مع الأدوات الأخرى

يعمل نظام التعاون الجماعي مع:
- ☁️ **التكامل السحابي**: GitHub PRs, Issues, Releases
- 📊 **إدارة المشاريع**: ربط المهام بالمساهمات
- 🔧 **Git الأساسي**: جميع عمليات Git المعتادة

---

**تم التطوير بواسطة:** Abdulaziz Alqudimi  
**الإصدار:** 3.0.0  
**المزيد من المساعدة:** استخدم `githydra team --help` لعرض جميع الخيارات
