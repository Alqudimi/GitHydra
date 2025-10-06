# مرجع API - GitHydra

<div dir="rtl">

## نظرة عامة

هذا المرجع يوثق جميع وحدات GitHydra ودوالها ووظائفها للمطورين الراغبين في استخدام GitHydra كمكتبة أو توسيعها.

## معلومات المشروع

**المطور:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**المستودع:** https://github.com/Alqudimi/GitHydra

## الوحدات الرئيسية

### src.logger

#### GitHydraLogger

```python
from src.logger import GitHydraLogger

class GitHydraLogger:
    """نظام السجلات لـ GitHydra"""
    
    def __init__(self, name: str = 'githydra'):
        """
        تهيئة نظام السجلات.
        
        Args:
            name: اسم المُسجِّل
        """
        
    def info(self, message: str):
        """سجل رسالة معلومات"""
        
    def debug(self, message: str):
        """سجل رسالة تصحيح"""
        
    def warning(self, message: str):
        """سجل رسالة تحذير"""
        
    def error(self, message: str):
        """سجل رسالة خطأ"""
```

**مثال:**
```python
from src.logger import get_logger

logger = get_logger(__name__)
logger.info("بدء العملية")
logger.error("حدث خطأ")
```

### src.utils.git_helper

#### get_repo()

```python
def get_repo(path: str = '.') -> git.Repo:
    """
    الحصول على كائن مستودع Git.
    
    Args:
        path: مسار المستودع (افتراضي: المجلد الحالي)
        
    Returns:
        git.Repo: كائن المستودع
        
    Raises:
        Exception: إذا لم يكن المسار مستودع Git
    """
```

**مثال:**
```python
from src.utils.git_helper import get_repo

repo = get_repo()
repo = get_repo('/path/to/repo')
```

#### is_repo_clean()

```python
def is_repo_clean(repo: git.Repo) -> bool:
    """
    التحقق من نظافة المستودع.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        bool: True إذا كان نظيفاً، False خلاف ذلك
    """
```

#### get_current_branch()

```python
def get_current_branch(repo: git.Repo) -> Optional[str]:
    """
    الحصول على اسم الفرع الحالي.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        str: اسم الفرع، أو None إذا كان detached HEAD
    """
```

#### get_modified_files()

```python
def get_modified_files(repo: git.Repo) -> List[str]:
    """
    الحصول على قائمة الملفات المعدلة.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        List[str]: قائمة مسارات الملفات المعدلة
    """
```

#### get_staged_files()

```python
def get_staged_files(repo: git.Repo) -> List[str]:
    """
    الحصول على قائمة الملفات المُجهزة.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        List[str]: قائمة مسارات الملفات المُجهزة
    """
```

### src.ui.console

#### print_panel()

```python
def print_panel(
    title: str,
    content: str,
    style: str = "cyan"
) -> None:
    """
    طباعة لوحة منسقة.
    
    Args:
        title: عنوان اللوحة
        content: محتوى اللوحة
        style: نمط اللون (cyan, green, red, yellow)
    """
```

**مثال:**
```python
from src.ui.console import print_panel

print_panel("النجاح", "العملية تمت بنجاح", "green")
print_panel("خطأ", "حدث خطأ", "red")
```

#### print_table()

```python
def print_table(
    headers: List[str],
    rows: List[List[str]],
    title: Optional[str] = None
) -> None:
    """
    طباعة جدول منسق.
    
    Args:
        headers: عناوين الأعمدة
        rows: صفوف البيانات
        title: عنوان الجدول (اختياري)
    """
```

**مثال:**
```python
from src.ui.console import print_table

headers = ["الاسم", "الفرع", "الالتزامات"]
rows = [
    ["أحمد", "main", "45"],
    ["فاطمة", "develop", "32"]
]
print_table(headers, rows, "المساهمون")
```

#### print_tree()

```python
def print_tree(
    label: str,
    items: Dict[str, Any]
) -> None:
    """
    طباعة شجرة منسقة.
    
    Args:
        label: عنوان الشجرة
        items: عناصر الشجرة (متداخلة)
    """
```

#### show_progress()

```python
@contextmanager
def show_progress(
    description: str,
    total: int
) -> Progress:
    """
    عرض شريط تقدم.
    
    Args:
        description: وصف العملية
        total: إجمالي الخطوات
        
    Yields:
        Progress: كائن التقدم
    """
```

**مثال:**
```python
from src.ui.console import show_progress

with show_progress("معالجة الملفات", 100) as progress:
    task = progress.add_task("processing", total=100)
    for i in range(100):
        # معالجة
        progress.update(task, advance=1)
```

## الأوامر

### src.commands.init

#### initialize_repo()

```python
def initialize_repo(
    path: str = '.',
    bare: bool = False
) -> git.Repo:
    """
    تهيئة مستودع Git جديد.
    
    Args:
        path: مسار المستودع
        bare: إنشاء مستودع bare
        
    Returns:
        git.Repo: المستودع المُنشأ
        
    Raises:
        Exception: إذا فشلت التهيئة
    """
```

### src.commands.status

#### get_status()

```python
def get_status(repo: git.Repo) -> Dict[str, Any]:
    """
    الحصول على حالة المستودع.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        Dict: معلومات الحالة
        {
            'branch': str,
            'is_clean': bool,
            'modified': List[str],
            'staged': List[str],
            'untracked': List[str]
        }
    """
```

### src.commands.branch

#### create_branch()

```python
def create_branch(
    repo: git.Repo,
    branch_name: str,
    start_point: Optional[str] = None
) -> git.Head:
    """
    إنشاء فرع جديد.
    
    Args:
        repo: كائن المستودع
        branch_name: اسم الفرع
        start_point: نقطة البداية (commit/branch)
        
    Returns:
        git.Head: الفرع المُنشأ
    """
```

#### delete_branch()

```python
def delete_branch(
    repo: git.Repo,
    branch_name: str,
    force: bool = False
) -> None:
    """
    حذف فرع.
    
    Args:
        repo: كائن المستودع
        branch_name: اسم الفرع
        force: حذف إجباري
    """
```

#### list_branches()

```python
def list_branches(
    repo: git.Repo,
    remote: bool = False
) -> List[str]:
    """
    عرض قائمة الفروع.
    
    Args:
        repo: كائن المستودع
        remote: عرض الفروع البعيدة
        
    Returns:
        List[str]: أسماء الفروع
    """
```

### src.commands.commit

#### create_commit()

```python
def create_commit(
    repo: git.Repo,
    message: str,
    amend: bool = False
) -> git.Commit:
    """
    إنشاء التزام.
    
    Args:
        repo: كائن المستودع
        message: رسالة الالتزام
        amend: تعديل آخر التزام
        
    Returns:
        git.Commit: الالتزام المُنشأ
    """
```

### src.commands.stage

#### stage_files()

```python
def stage_files(
    repo: git.Repo,
    files: List[str],
    all_files: bool = False
) -> None:
    """
    تجهيز ملفات.
    
    Args:
        repo: كائن المستودع
        files: قائمة الملفات
        all_files: تجهيز جميع الملفات
    """
```

#### unstage_files()

```python
def unstage_files(
    repo: git.Repo,
    files: List[str]
) -> None:
    """
    إلغاء تجهيز ملفات.
    
    Args:
        repo: كائن المستودع
        files: قائمة الملفات
    """
```

### src.commands.sync

#### push_changes()

```python
def push_changes(
    repo: git.Repo,
    remote: str = 'origin',
    branch: Optional[str] = None,
    force: bool = False
) -> None:
    """
    دفع التغييرات.
    
    Args:
        repo: كائن المستودع
        remote: اسم المستودع البعيد
        branch: اسم الفرع
        force: دفع إجباري
    """
```

#### pull_changes()

```python
def pull_changes(
    repo: git.Repo,
    remote: str = 'origin',
    branch: Optional[str] = None,
    rebase: bool = False
) -> None:
    """
    سحب التغييرات.
    
    Args:
        repo: كائن المستودع
        remote: اسم المستودع البعيد
        branch: اسم الفرع
        rebase: استخدام rebase
    """
```

### src.commands.statistics

#### get_repository_stats()

```python
def get_repository_stats(
    repo: git.Repo
) -> Dict[str, Any]:
    """
    الحصول على إحصائيات المستودع.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        Dict: الإحصائيات
        {
            'total_commits': int,
            'total_files': int,
            'total_contributors': int,
            'branches': int,
            'tags': int
        }
    """
```

#### get_contributor_stats()

```python
def get_contributor_stats(
    repo: git.Repo
) -> List[Dict[str, Any]]:
    """
    الحصول على إحصائيات المساهمين.
    
    Args:
        repo: كائن المستودع
        
    Returns:
        List[Dict]: قائمة المساهمين مع إحصائياتهم
    """
```

## الاستثناءات

### GitHydraError

```python
class GitHydraError(Exception):
    """استثناء أساسي لـ GitHydra"""
    pass
```

### RepositoryNotFoundError

```python
class RepositoryNotFoundError(GitHydraError):
    """المستودع غير موجود"""
    pass
```

### BranchNotFoundError

```python
class BranchNotFoundError(GitHydraError):
    """الفرع غير موجود"""
    pass
```

### CommitError

```python
class CommitError(GitHydraError):
    """خطأ في الالتزام"""
    pass
```

## الثوابت

### src.constants

```python
# المسارات
HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / '.githydra'
LOG_DIR = CONFIG_DIR / 'logs'
CONFIG_FILE = CONFIG_DIR / 'config.yaml'
ALIASES_FILE = CONFIG_DIR / 'aliases.yaml'

# الإصدار
VERSION = '3.0'

# الألوان
COLORS = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan'
}

# إعدادات افتراضية
DEFAULT_CONFIG = {
    'log_level': 'INFO',
    'color_output': True,
    'default_branch': 'main'
}
```

## أمثلة متقدمة

### مثال 1: إنشاء أمر مخصص

```python
from src.utils.git_helper import get_repo
from src.ui.console import print_panel, print_table
from src.logger import get_logger

logger = get_logger(__name__)

def custom_status():
    """عرض حالة مخصصة"""
    try:
        repo = get_repo()
        
        # جمع المعلومات
        branch = repo.active_branch.name
        modified = [item.a_path for item in repo.index.diff(None)]
        staged = [item.a_path for item in repo.index.diff('HEAD')]
        
        # عرض النتائج
        print_panel(
            f"حالة المستودع - {branch}",
            f"معدلة: {len(modified)}, مُجهزة: {len(staged)}",
            "cyan"
        )
        
        if modified or staged:
            rows = []
            for file in modified:
                rows.append([file, "معدل", "غير مُجهز"])
            for file in staged:
                rows.append([file, "مُجهز", "جاهز للالتزام"])
                
            print_table(["الملف", "الحالة", "الملاحظات"], rows)
            
        logger.info("عُرضت الحالة المخصصة")
        
    except Exception as e:
        logger.error(f"خطأ: {e}")
        raise
```

### مثال 2: معالجة مجمعة للفروع

```python
from src.utils.git_helper import get_repo
from src.commands.branch import delete_branch
from src.ui.console import show_progress

def cleanup_merged_branches():
    """حذف الفروع المدمجة"""
    repo = get_repo()
    main_branch = 'main'
    
    # الحصول على الفروع المدمجة
    merged_branches = [
        b for b in repo.branches
        if b.name != main_branch and 
        repo.is_ancestor(b.commit, repo.branches[main_branch].commit)
    ]
    
    with show_progress("حذف الفروع", len(merged_branches)) as progress:
        task = progress.add_task("cleanup", total=len(merged_branches))
        
        for branch in merged_branches:
            delete_branch(repo, branch.name)
            progress.update(task, advance=1)
```

### مثال 3: تحليل مخصص

```python
from collections import defaultdict
from datetime import datetime
from src.utils.git_helper import get_repo

def analyze_commit_frequency():
    """تحليل تكرار الالتزامات"""
    repo = get_repo()
    frequency = defaultdict(int)
    
    for commit in repo.iter_commits():
        date = datetime.fromtimestamp(commit.committed_date)
        day = date.strftime('%Y-%m-%d')
        frequency[day] += 1
    
    return dict(sorted(frequency.items()))
```

## الدعم والمساهمة

للحصول على مساعدة أو المساهمة:

**المطور:** عبدالعزيز القديمي  
**البريد الإلكتروني:** eng7mi@gmail.com  
**GitHub:** https://github.com/Alqudimi/GitHydra  
**التوثيق:** https://github.com/Alqudimi/GitHydra/tree/main/docs

</div>
