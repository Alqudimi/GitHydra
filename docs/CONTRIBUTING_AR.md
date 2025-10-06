# دليل المساهمة - GitHydra

<div dir="rtl">

## مرحباً بك في مجتمع GitHydra!

نشكرك على اهتمامك بالمساهمة في GitHydra. هذا الدليل سيساعدك على البدء في المساهمة بفعالية.

## معلومات المشروع

**المشرف الرئيسي:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra  
**الترخيص:** MIT

## طرق المساهمة

يمكنك المساهمة بعدة طرق:

### 1. الإبلاغ عن الأخطاء
- ابحث أولاً في Issues الموجودة
- استخدم قالب تقرير الخطأ
- قدم معلومات تفصيلية عن المشكلة

### 2. اقتراح ميزات جديدة
- افتح Issue جديد
- اشرح الميزة المقترحة بالتفصيل
- وضح الفائدة المرجوة

### 3. تحسين التوثيق
- تصحيح الأخطاء الإملائية
- إضافة أمثلة
- ترجمة إلى لغات أخرى

### 4. كتابة الكود
- إصلاح الأخطاء
- تطوير ميزات جديدة
- تحسين الأداء

## إعداد بيئة التطوير

### الخطوة 1: Fork المستودع
```bash
# انتقل إلى GitHub وانقر على Fork
# ثم استنسخ Fork الخاص بك
git clone https://github.com/YOUR_USERNAME/GitHydra.git
cd GitHydra
```

### الخطوة 2: إعداد البيئة الافتراضية
```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# على Linux/Mac:
source venv/bin/activate
# على Windows:
venv\Scripts\activate
```

### الخطوة 3: تثبيت المتطلبات
```bash
# تثبيت المتطلبات الأساسية
pip install -r requirements.txt

# تثبيت المتطلبات التطويرية (إن وُجدت)
pip install -r requirements-dev.txt

# تثبيت GitHydra في وضع التطوير
pip install -e .
```

### الخطوة 4: إضافة المستودع الأصلي
```bash
git remote add upstream https://github.com/Alqudimi/GitHydra.git
```

## سير عمل المساهمة

### 1. المزامنة مع المستودع الأصلي
```bash
git fetch upstream
git checkout main
git merge upstream/main
```

### 2. إنشاء فرع للميزة
```bash
# استخدم اسماً وصفياً
git checkout -b feature/amazing-feature
# أو
git checkout -b fix/bug-description
# أو
git checkout -b docs/documentation-improvement
```

### 3. إجراء التغييرات

#### إرشادات كتابة الكود
- اتبع PEP 8 لتنسيق Python
- استخدم أسماء متغيرات واضحة
- أضف تعليقات توضيحية
- اجعل الدوال صغيرة ومركزة

#### مثال على كود جيد:
```python
def calculate_commit_statistics(repo, branch_name='main'):
    """
    حساب إحصائيات الالتزامات لفرع معين.
    
    Args:
        repo: كائن المستودع
        branch_name: اسم الفرع (افتراضي: main)
        
    Returns:
        dict: إحصائيات الالتزامات
    """
    try:
        commits = list(repo.iter_commits(branch_name))
        return {
            'total_commits': len(commits),
            'authors': len(set(c.author.name for c in commits))
        }
    except Exception as e:
        logger.error(f"خطأ في حساب الإحصائيات: {e}")
        raise
```

### 4. كتابة الاختبارات

```python
# tests/test_statistics.py
import pytest
from src.commands.statistics import calculate_commit_statistics

def test_calculate_statistics(test_repo):
    """اختبار حساب الإحصائيات"""
    stats = calculate_commit_statistics(test_repo)
    assert 'total_commits' in stats
    assert 'authors' in stats
    assert stats['total_commits'] >= 0
```

### 5. التأكد من جودة الكود

```bash
# تنسيق الكود
black src/ tests/

# فحص الجودة
pylint src/

# تشغيل الاختبارات
pytest tests/
```

### 6. إنشاء Commit

```bash
# تجهيز التغييرات
git add .

# إنشاء commit برسالة واضحة
git commit -m "نوع: وصف مختصر

وصف تفصيلي للتغييرات إذا لزم الأمر.

Fixes #123"
```

#### أنواع Commits:
- `feat:` ميزة جديدة
- `fix:` إصلاح خطأ
- `docs:` تحديث توثيق
- `style:` تنسيق كود
- `refactor:` إعادة هيكلة
- `test:` إضافة اختبارات
- `chore:` مهام صيانة

### 7. الدفع إلى Fork
```bash
git push origin feature/amazing-feature
```

### 8. فتح Pull Request

1. انتقل إلى المستودع على GitHub
2. انقر على "New Pull Request"
3. اختر فرعك
4. املأ نموذج PR:
   - عنوان واضح
   - وصف التغييرات
   - إشارة إلى Issues ذات الصلة
   - لقطات شاشة إن أمكن

#### نموذج Pull Request:

```markdown
## الوصف
وصف مختصر للتغييرات المقترحة.

## نوع التغيير
- [ ] إصلاح خطأ
- [ ] ميزة جديدة
- [ ] تغيير مُحطِّم (breaking change)
- [ ] تحديث توثيق

## كيف تم الاختبار؟
صف الاختبارات التي أجريتها.

## قائمة التحقق
- [ ] الكود يتبع إرشادات المشروع
- [ ] راجعت الكود الخاص بي
- [ ] التعليقات واضحة
- [ ] التوثيق محدّث
- [ ] لا توجد تحذيرات جديدة
- [ ] الاختبارات تمر بنجاح

## لقطات الشاشة (إن وُجدت)

## الملاحظات الإضافية
```

## معايير المراجعة

سيتم مراجعة Pull Request الخاص بك بناءً على:

### 1. جودة الكود
- الوضوح والقراءة
- اتباع المعايير
- معالجة الأخطاء
- الأداء

### 2. الاختبارات
- تغطية كافية
- حالات الحافة
- اختبارات واضحة

### 3. التوثيق
- التعليقات في الكود
- تحديث الـ README
- تحديث دليل المستخدم

### 4. التوافق
- يعمل مع الإصدارات المدعومة
- لا يكسر الوظائف الموجودة
- متوافق مع المنصات المختلفة

## إرشادات محددة

### إضافة أمر جديد

1. **أنشئ الملف:**
```python
# src/commands/newcommand.py
import click
from src.utils.git_helper import get_repo
from src.ui.console import console

@click.command()
def newcommand():
    """وصف الأمر الجديد"""
    try:
        repo = get_repo()
        # منطق الأمر
        console.print("[green]نجح![/green]")
    except Exception as e:
        console.print(f"[red]خطأ: {e}[/red]")
```

2. **سجّل الأمر:**
```python
# githydra.py
from src.commands import newcommand
cli.add_command(newcommand.newcommand)
```

3. **أضف للقائمة التفاعلية:**
```python
# src/commands/interactive.py
MAIN_MENU = {
    # ...
    'N': ('الفئة', [
        ('1', 'الأمر الجديد', 'newcommand'),
    ]),
}
```

4. **حدّث التوثيق:**
- أضف في `docs/USER_GUIDE_AR.md`
- أضف في `README.md`

### تحسين الأداء

1. **قِس الأداء أولاً:**
```python
import time

start = time.time()
# العملية
duration = time.time() - start
print(f"الوقت المستغرق: {duration}s")
```

2. **حسّن:**
- استخدم التخزين المؤقت
- قلل استدعاءات Git
- استخدم عمليات مجمعة

3. **قِس مجدداً:**
- تأكد من التحسين
- وثّق النتائج

### إصلاح الأخطاء

1. **أعد إنتاج الخطأ:**
```python
def test_bug_reproduction():
    """اختبار يعيد إنتاج الخطأ"""
    # خطوات إعادة الإنتاج
    result = buggy_function()
    assert result == expected  # سيفشل
```

2. **أصلح:**
```python
def buggy_function():
    # الكود المُصلح
    pass
```

3. **اختبر:**
```python
def test_bug_fixed():
    """اختبار التأكد من الإصلاح"""
    result = buggy_function()
    assert result == expected  # سينجح
```

## قواعد السلوك

### كن محترماً
- احترم المساهمين الآخرين
- كن بناءً في النقد
- رحب بالمبتدئين

### التواصل الفعال
- كن واضحاً في الشرح
- اطرح الأسئلة عند عدم الفهم
- شارك المعرفة

### الالتزام بالمعايير
- اتبع إرشادات المشروع
- احترم قرارات المشرفين
- ساعد في الحفاظ على الجودة

## الحصول على المساعدة

### القنوات المتاحة

1. **GitHub Issues:**
   - للأسئلة التقنية
   - للإبلاغ عن المشاكل
   - https://github.com/Alqudimi/GitHydra/issues

2. **البريد الإلكتروني:**
   - للاستفسارات الخاصة
   - eng7mi@gmail.com

3. **التوثيق:**
   - راجع `docs/` للأدلة
   - اقرأ الكود المصدري

### أسئلة شائعة للمساهمين

**س: كم يستغرق مراجعة PR؟**
ج: عادةً خلال أسبوع، حسب حجم التغيير.

**س: هل يمكنني العمل على أكثر من ميزة؟**
ج: نعم، لكن أنشئ PR منفصل لكل ميزة.

**س: ماذا لو رُفض PR الخاص بي؟**
ج: راجع التعليقات، حسّن التغييرات، وأعد التقديم.

**س: كيف أصبح مساهماً منتظماً؟**
ج: ساهم باستمرار وبجودة عالية.

## الاعتراف بالمساهمين

نقدر جميع المساهمات ونعترف بالمساهمين:

- قائمة في README.md
- شكر في release notes
- الإشارة في التوثيق

## الترخيص

بالمساهمة في GitHydra، فإنك توافق على أن مساهماتك ستُرخص بموجب ترخيص MIT.

## شكراً لك!

مساهمتك تجعل GitHydra أفضل للجميع. نقدر وقتك وجهدك!

**المشرف:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra

</div>
