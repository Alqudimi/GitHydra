# دليل المطور - GitHydra

<div dir="rtl">

## نظرة عامة

هذا الدليل مخصص للمطورين الراغبين في فهم البنية الداخلية لـ GitHydra والمساهمة في تطويرها.

## معلومات المطور

**المطور الرئيسي:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra

## البنية المعمارية

### هيكل المشروع

```
GitHydra/
├── githydra.py              # نقطة الدخول الرئيسية
├── pyproject.toml           # تكوين حزمة Python
├── requirements.txt         # المتطلبات
├── LICENSE                  # ترخيص MIT
├── README.md                # التوثيق الرئيسي
├── QUICKSTART.md            # دليل البدء السريع
├── install.sh               # سكريبت تثبيت Linux/Mac
├── install.bat              # سكريبت تثبيت Windows
├── docs/                    # التوثيق
│   ├── README_AR.md
│   ├── INSTALLATION_AR.md
│   ├── USER_GUIDE_AR.md
│   └── DEVELOPER_GUIDE_AR.md
└── src/
    ├── __init__.py
    ├── logger.py            # نظام السجلات
    ├── commands/            # تنفيذ الأوامر
    │   ├── __init__.py
    │   ├── init.py          # تهيئة المستودع
    │   ├── status.py        # حالة المستودع
    │   ├── branch.py        # إدارة الفروع
    │   ├── commit.py        # عمليات الالتزام
    │   ├── remote.py        # المستودعات البعيدة
    │   ├── log.py           # عرض السجل
    │   ├── stage.py         # منطقة التجهيز
    │   ├── sync.py          # المزامنة
    │   ├── interactive.py   # الواجهة التفاعلية
    │   ├── repair.py        # الصيانة والإصلاح
    │   ├── stash.py         # المخبأ
    │   ├── tag.py           # الوسوم
    │   ├── reset.py         # إعادة التعيين
    │   ├── diff.py          # عرض الفروقات
    │   ├── config.py        # التكوين
    │   ├── alias.py         # الأوامر المختصرة
    │   ├── submodule.py     # الوحدات الفرعية
    │   ├── worktree.py      # أشجار العمل
    │   ├── reflog.py        # سجل المراجع
    │   ├── bisect.py        # البحث الثنائي
    │   ├── blame.py         # معلومات المؤلف
    │   ├── archive.py       # الأرشفة
    │   ├── clean.py         # التنظيف
    │   ├── notes.py         # الملاحظات
    │   ├── patch.py         # التصحيحات
    │   ├── statistics.py    # الإحصائيات
    │   ├── conflicts.py     # حل النزاعات
    │   ├── rebase.py        # إعادة الأساس
    │   ├── bundle.py        # الحزم
    │   └── compare.py       # المقارنة
    ├── ui/
    │   ├── __init__.py
    │   └── console.py       # مكونات واجهة المستخدم
    └── utils/
        ├── __init__.py
        └── git_helper.py    # وظائف مساعدة Git
```

## المكونات الرئيسية

### 1. نقطة الدخول (githydra.py)

```python
import click
from src.commands import *

@click.group()
@click.version_option(version='3.0', prog_name='GitHydra')
def cli():
    """GitHydra - أداة CLI شاملة لأتمتة Git"""
    pass

# تسجيل جميع الأوامر
cli.add_command(init.init)
cli.add_command(status.status)
# ... المزيد من الأوامر
```

### 2. نظام السجلات (logger.py)

يوفر تسجيلاً شاملاً لجميع العمليات:

```python
import logging
from pathlib import Path
from datetime import datetime

class GitHydraLogger:
    def __init__(self):
        self.log_dir = Path.home() / '.githydra' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
    def setup_logger(self, name):
        logger = logging.getLogger(name)
        # إعداد معالجات السجل
        return logger
```

### 3. مكونات واجهة المستخدم (ui/console.py)

تستخدم Rich لإنشاء واجهة جميلة:

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def print_panel(title, content, style="cyan"):
    panel = Panel(content, title=title, border_style=style)
    console.print(panel)

def print_table(headers, rows):
    table = Table()
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*row)
    console.print(table)
```

### 4. وظائف Git المساعدة (utils/git_helper.py)

```python
from git import Repo
from pathlib import Path

def get_repo(path='.'):
    try:
        return Repo(path, search_parent_directories=True)
    except Exception as e:
        raise Exception(f"ليس مستودع Git: {e}")

def is_repo_clean(repo):
    return not repo.is_dirty()

def get_current_branch(repo):
    try:
        return repo.active_branch.name
    except:
        return None
```

## إضافة أمر جديد

### الخطوة 1: إنشاء ملف الأمر

أنشئ ملفاً جديداً في `src/commands/`:

```python
# src/commands/mycommand.py
import click
from src.utils.git_helper import get_repo
from src.ui.console import console, print_panel
from src.logger import get_logger

logger = get_logger(__name__)

@click.command()
@click.option('--option', help='وصف الخيار')
def mycommand(option):
    """وصف الأمر الجديد"""
    try:
        repo = get_repo()
        logger.info(f"تنفيذ mycommand مع الخيار: {option}")
        
        # منطق الأمر هنا
        result = do_something(repo, option)
        
        print_panel("النتيجة", result, "green")
        logger.info("نجح mycommand")
        
    except Exception as e:
        console.print(f"[red]خطأ: {e}[/red]")
        logger.error(f"فشل mycommand: {e}")

def do_something(repo, option):
    # تنفيذ الأمر
    return "تم بنجاح"
```

### الخطوة 2: تسجيل الأمر

أضف الأمر إلى `githydra.py`:

```python
from src.commands import mycommand

cli.add_command(mycommand.mycommand)
```

### الخطوة 3: إضافة للقائمة التفاعلية

عدّل `src/commands/interactive.py`:

```python
MAIN_MENU = {
    # ... قوائم موجودة
    'N': ('فئة جديدة', [
        ('1', 'الأمر الجديد', 'mycommand --option value'),
    ]),
}
```

## المكتبات المستخدمة

### 1. Click
- إطار عمل CLI قوي
- تحليل الأوامر والخيارات
- التوثيق التلقائي

```python
@click.command()
@click.option('--name', prompt='الاسم', help='اسم المستخدم')
@click.argument('file', type=click.Path(exists=True))
def cmd(name, file):
    pass
```

### 2. Rich
- واجهة طرفية جميلة
- جداول وألواح وأشرطة تقدم
- تنسيق وألوان

```python
from rich.console import Console
from rich.progress import track

console = Console()
console.print("[bold cyan]رسالة[/bold cyan]")

for item in track(items, description="معالجة..."):
    process(item)
```

### 3. GitPython
- واجهة Python لـ Git
- عمليات المستودع
- فحص التاريخ والفروع

```python
from git import Repo

repo = Repo('.')
commits = list(repo.iter_commits('main', max_count=10))
branches = [b.name for b in repo.branches]
```

### 4. Questionary
- مطالبات تفاعلية
- اختيار من قوائم
- إدخال نصي محسّن

```python
import questionary

answer = questionary.select(
    "اختر خياراً:",
    choices=['خيار 1', 'خيار 2', 'خيار 3']
).ask()
```

### 5. PyYAML
- قراءة وكتابة YAML
- ملفات التكوين
- الأوامر المختصرة

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

## أفضل الممارسات

### 1. معالجة الأخطاء

```python
try:
    # محاولة العملية
    result = risky_operation()
except GitCommandError as e:
    # خطأ Git محدد
    logger.error(f"خطأ Git: {e}")
    console.print(f"[red]فشلت عملية Git: {e}[/red]")
except Exception as e:
    # خطأ عام
    logger.error(f"خطأ غير متوقع: {e}")
    console.print(f"[red]خطأ: {e}[/red]")
```

### 2. التسجيل

```python
# سجّل جميع العمليات المهمة
logger.info("بدء العملية X")
logger.debug(f"التفاصيل: {details}")
logger.warning("تحذير: Y")
logger.error(f"خطأ: {error}")
```

### 3. واجهة المستخدم

```python
# استخدم Rich لعرض جميل
from rich.console import Console
from rich.progress import Progress

console = Console()

with Progress() as progress:
    task = progress.add_task("[cyan]معالجة...", total=100)
    # العملية
    progress.update(task, advance=10)
```

### 4. الاختبار

```python
# اختبر الأوامر قبل الدمج
def test_mycommand():
    repo = create_test_repo()
    result = mycommand_logic(repo)
    assert result == expected_value
```

## التكوين والإعدادات

### ملف التكوين (~/.githydra/config.yaml)

```yaml
# إعدادات عامة
general:
  log_level: INFO
  color_output: true
  default_branch: main

# إعدادات العرض
display:
  show_graph: true
  max_log_entries: 50
  date_format: "%Y-%m-%d %H:%M"

# إعدادات Git
git:
  auto_stage: false
  auto_fetch: true
  push_default: simple
```

### الأوامر المختصرة (~/.githydra/aliases.yaml)

```yaml
aliases:
  st: status
  co: commit
  br: branch
  sw: branch switch
  pl: sync pull
  ps: sync push
```

## نظام السجلات

### موقع السجلات
```
~/.githydra/logs/
├── 2025-10-06.log
├── 2025-10-05.log
└── ...
```

### تنسيق السجل
```
2025-10-06 14:30:45 - INFO - [init] تهيئة مستودع جديد
2025-10-06 14:31:12 - INFO - [commit] إنشاء التزام: رسالة الالتزام
2025-10-06 14:31:45 - ERROR - [push] فشل الدفع: Authentication failed
```

## الاختبار

### اختبار يدوي

```bash
# اختبر التثبيت
pip install -e .

# اختبر الأوامر الأساسية
githydra --version
githydra --help
githydra interactive

# اختبر أمر محدد
githydra init test-repo
cd test-repo
githydra status
```

### اختبار آلي (مستقبلي)

```python
# tests/test_commands.py
import pytest
from src.commands import init, status

def test_init_creates_repo(tmp_path):
    repo_path = tmp_path / "test-repo"
    init.initialize_repo(str(repo_path))
    assert (repo_path / ".git").exists()

def test_status_shows_clean(test_repo):
    result = status.get_status(test_repo)
    assert result.is_clean == True
```

## المساهمة

### خطوات المساهمة

1. **Fork المستودع**
```bash
# Fork على GitHub ثم
git clone https://github.com/YOUR_USERNAME/GitHydra.git
cd GitHydra
```

2. **إنشاء فرع للميزة**
```bash
githydra branch create feature/amazing-feature
```

3. **إجراء التغييرات**
```bash
# تعديل الكود
githydra stage add --all
githydra commit -m "إضافة ميزة رائعة"
```

4. **الدفع والـ Pull Request**
```bash
githydra sync push origin feature/amazing-feature
# افتح Pull Request على GitHub
```

### إرشادات الكود

- اتبع PEP 8 لتنسيق Python
- أضف تعليقات توضيحية
- سجّل جميع العمليات المهمة
- اختبر الكود قبل الدمج
- حدّث التوثيق

## الأسئلة الشائعة للمطورين

### كيف أضيف لغة جديدة للتوثيق؟
أنشئ ملفات جديدة في مجلد `docs/` بلاحقة اللغة (مثل `_FR.md` للفرنسية).

### كيف أحسّن الأداء؟
- استخدم التخزين المؤقت للعمليات المتكررة
- قلل استدعاءات Git غير الضرورية
- استخدم العمليات المجمعة عند الإمكان

### كيف أضيف دعم لمنصة جديدة؟
عدّل سكريبتات التثبيت وتأكد من توافق المتطلبات.

## موارد إضافية

### المراجع
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
- [Git Documentation](https://git-scm.com/doc)

### الأدوات المفيدة
- **Black**: تنسيق كود Python
- **Pylint**: فحص جودة الكود
- **pytest**: إطار اختبار
- **mypy**: فحص الأنواع

## الاتصال والدعم

للأسئلة التقنية أو المساهمات:

**المطور:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**GitHub:** https://github.com/Alqudimi/GitHydra  
**Issues:** https://github.com/Alqudimi/GitHydra/issues

</div>
