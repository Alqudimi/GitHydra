# GitHydra 

<p align="center">
  <a href="https://github.com/Alqudimi/GitHydra">
    <img src="assets/images/logo.png" alt="شعار المشروع" width="450" height="450">
  </a>
</p>

<h1 align="center">GitHydra</h1>

<p align="center">
  وصف قوي وجذاب لمشروعك في جملة أو اثنتين. is a powerful Python-based command-line tool that transforms Git into an intuitive, beautiful experience. Built with Rich for stunning terminal UI, Click for robust CLI framework, and GitPython for seamless Git integration.
  <br />
  <a href="https://github.com/Alqudimi/GitHydra/doc"><strong>استكشف الوثائق »</strong></a>
  <br />
  <br />
  <a href="https://github.com/Alqudimi/GitHydra/issues">الإبلاغ عن خطأ</a>
  ·
  <a href="https://github.com/Alqudimi/GitHydra/issues">طلب ميزة</a>
</p>

<p align="center">
  <a href="https://github.com/Alqudimi/GitHydra/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="الترخيص">
  </a>
  <a href="https://github.com/Abdulaziz/GitHydra/releases">
    <img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="الإصدار">
  </a>
  <a href="https://github.com/Alqudimi/GitHydra/stargazers">
    <img src="https://img.shields.io/github/stars/Alqudimi/GitHydra.svg?style=social" alt="النجوم">
  </a>
</p>

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**أداة شاملة لإدارة Git مع واجهة طرفية جميلة**

**Comprehensive Git Automation CLI Tool with Beautiful Terminal UI**

[English](#english) | [العربية](#arabic)

</div>

---

## <a name="english"></a>English Documentation

### ✨ Features

**13 Feature Categories | 33 Command Groups | 70+ Operations**

#### 1️⃣ Repository Operations
- Initialize repositories
- View detailed status
- Clone with progress tracking

#### 2️⃣ File & Staging
- Interactive staging area
- Smart file selection
- Stage/unstage management

#### 3️⃣ Commits & History
- Beautiful commit creation
- Rich history viewer with graph
- Advanced search and filtering

#### 4️⃣ Branches
- Create, delete, rename branches
- Switch branches seamlessly
- Track remote branches

#### 5️⃣ Remote & Sync
- Manage remotes
- Push/pull/fetch operations
- Smart sync strategies

#### 6️⃣ Advanced Operations
- Stash management
- Tag creation
- Reset, revert, cherry-pick
- Enhanced diff viewer

#### 7️⃣ Submodules & Worktrees
- **Submodules**: add, init, update, status, sync, foreach, deinit
- **Worktrees**: create multiple working trees, list, remove, prune, lock/unlock, move

#### 8️⃣ Debugging & Search
- **Bisect**: Binary search to find bugs
- **Blame**: Line-by-line authorship with statistics
- **Reflog**: View and manage reference logs

#### 9️⃣ Patches & Bundles
- **Patches**: Create, apply, format patches
- **Bundles**: Transport repositories via bundle files

#### 🅰️ Conflicts & Merging
- List conflicted files
- Accept ours/theirs strategies
- Launch merge tools
- Abort operations safely

#### 🅱️ Statistics & Analysis
- Repository overview
- Contributor statistics
- Activity analysis
- File statistics
- Language distribution

#### ©️ Maintenance & Repair
- Archive creation (zip, tar, tar.gz)
- Clean untracked files
- Repository integrity checks
- Garbage collection

#### 🅳 Configuration
- Git config management
- Command aliases
- User preferences

### 📦 Installation

#### Quick Install
```bash
pip install -e .
pip install githydra 
```

#### Manual Installation
```bash
git clone https://github.com/Alqudimi/GitHydra.git
cd githydra
pip install -r requirements.txt
```

### 🎯 Usage

#### Interactive Mode (Recommended)
```bash
githydra interactive
# or
python githydra.py interactive
```

#### Command Line Mode
```bash
githydra status
githydra commit -m "Your message"
githydra branch list
githydra log --graph
githydra submodule add <url>
githydra statistics overview
githydra compare branches main develop
```

#### Available Commands
```bash
githydra --help
githydra <command> --help
```

### 📋 Command Examples

#### Repository Operations
```bash
githydra init [path]              # Initialize repository
githydra status                   # Show status
githydra clone <url>              # Clone repository
```

#### Staging & Commits
```bash
githydra stage add --interactive  # Interactive staging
githydra commit -m "message"      # Create commit
githydra log --graph --limit 20   # View history
```

#### Branch Management
```bash
githydra branch create feature    # Create branch
githydra branch switch develop    # Switch branch
githydra branch delete old-branch # Delete branch
```

#### Remote Operations
```bash
githydra remote add origin <url>  # Add remote
githydra sync push                # Push changes
githydra sync pull                # Pull changes
```

#### Advanced Features
```bash
githydra stash save -m "WIP"      # Stash changes
githydra tag create v1.0          # Create tag
githydra bisect start             # Start bisect
githydra blame src/main.py        # Show authorship
githydra archive create --format zip  # Create archive
```

#### Statistics & Analysis
```bash
githydra statistics overview      # Repository stats
githydra statistics contributors  # Contributor stats
githydra statistics activity      # Activity analysis
```

#### Debugging Tools
```bash
githydra bisect start             # Find bugs
githydra blame <file>             # Line authorship
githydra reflog show              # View reflog
```

### 🎨 Features Highlights

- **Beautiful UI**: Rich terminal interface with colors, tables, and progress bars
- **Interactive Menus**: User-friendly navigation through all features
- **Comprehensive Logging**: All operations logged to `~/.githydra/logs/`
- **Smart Error Handling**: Graceful error messages and recovery
- **Configuration**: Customizable via `~/.githydra/config.yaml`
- **Aliases**: Create shortcuts for frequent commands
- **Progress Tracking**: Visual feedback for long operations
- **Git Integration**: Seamless GitPython backend

### 📁 Project Structure

```
githydra/
├── githydra.py              # Main entry point
├── src/
│   ├── commands/            # All command implementations
│   ├── ui/                  # Rich UI components
│   ├── utils/               # Utility functions
│   └── logger.py            # Logging system
├── setup.py                 # Installation script
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### 🔧 Configuration

GitHydra stores configuration in `~/.githydra/`:
- `config.yaml` - User preferences
- `aliases.yaml` - Command aliases
- `logs/` - Operation logs by date

### 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### 📄 License

MIT License - Feel free to use and modify.

### 🐛 Bug Reports

Found a bug? Please open an issue with:
- GitHydra version
- Python version
- Error message
- Steps to reproduce

---

## <a name="arabic"></a>التوثيق العربي

### 🚀 نظرة عامة

GitHydra هي أداة قوية مبنية على Python لإدارة Git بواجهة طرفية جميلة وسهلة الاستخدام. مبنية باستخدام Rich لواجهة المستخدم، Click لإطار CLI، وGitPython للتكامل مع Git.

### ✨ المميزات

**13 فئة | 33 مجموعة أوامر | أكثر من 70 عملية**

#### 1️⃣ عمليات المستودع
- تهيئة المستودعات
- عرض الحالة التفصيلية
- الاستنساخ مع تتبع التقدم

#### 2️⃣ الملفات والتجهيز
- منطقة تجهيز تفاعلية
- اختيار ذكي للملفات
- إدارة التجهيز/إلغاء التجهيز

#### 3️⃣ الالتزامات والتاريخ
- إنشاء التزامات جميلة
- عارض تاريخ غني بالرسوم البيانية
- البحث والتصفية المتقدمة

#### 4️⃣ الفروع
- إنشاء وحذف وإعادة تسمية الفروع
- التبديل بين الفروع بسلاسة
- تتبع الفروع البعيدة

#### 5️⃣ البعيد والمزامنة
- إدارة المستودعات البعيدة
- عمليات الدفع/السحب/الجلب
- استراتيجيات المزامنة الذكية

#### 6️⃣ العمليات المتقدمة
- إدارة التخزين المؤقت
- إنشاء الوسوم
- إعادة التعيين والاستعادة واختيار الكرز
- عارض الفروقات المحسّن

#### 7️⃣ الوحدات الفرعية وأشجار العمل
- **الوحدات الفرعية**: إضافة، تهيئة، تحديث، حالة، مزامنة
- **أشجار العمل**: إنشاء أشجار عمل متعددة، قائمة، إزالة

#### 8️⃣ التصحيح والبحث
- **Bisect**: بحث ثنائي لإيجاد الأخطاء
- **Blame**: معرفة من كتب كل سطر
- **Reflog**: عرض وإدارة سجلات المراجع

#### 9️⃣ التصحيحات والحزم
- **التصحيحات**: إنشاء وتطبيق التصحيحات
- **الحزم**: نقل المستودعات عبر ملفات الحزم

#### 🅰️ التعارضات والدمج
- قائمة الملفات المتعارضة
- قبول استراتيجيات "لنا" أو "لهم"
- تشغيل أدوات الدمج
- إلغاء العمليات بأمان

#### 🅱️ الإحصائيات والتحليلات
- نظرة عامة على المستودع
- إحصائيات المساهمين
- تحليل النشاط
- إحصائيات الملفات
- توزيع اللغات

#### ©️ الصيانة والإصلاح
- إنشاء الأرشيفات (zip, tar, tar.gz)
- تنظيف الملفات غير المتتبعة
- فحص سلامة المستودع
- جمع القمامة

#### 🅳 التكوين
- إدارة إعدادات Git
- الاختصارات
- تفضيلات المستخدم

### 📦 التثبيت

#### التثبيت السريع
```bash
pip install -e .
pip install githydra 
```

#### التثبيت اليدوي
```bash
git clone https://github.com/Alqudimi/GitHydra.git
cd githydra
pip install -r requirements.txt
```

### 🎯 الاستخدام

#### الوضع التفاعلي (موصى به)
```bash
githydra interactive
# أو
python githydra.py interactive
```

#### وضع سطر الأوامر
```bash
githydra status
githydra commit -m "رسالتك"
githydra branch list
githydra log --graph
githydra submodule add <url>
githydra statistics overview
```

### 📋 أمثلة الأوامر

#### عمليات المستودع
```bash
githydra init [path]              # تهيئة مستودع
githydra status                   # عرض الحالة
githydra clone <url>              # استنساخ مستودع
```

#### التجهيز والالتزامات
```bash
githydra stage add --interactive  # تجهيز تفاعلي
githydra commit -m "الرسالة"      # إنشاء التزام
githydra log --graph --limit 20   # عرض التاريخ
```

#### إدارة الفروع
```bash
githydra branch create feature    # إنشاء فرع
githydra branch switch develop    # التبديل للفرع
githydra branch delete old-branch # حذف فرع
```

#### العمليات البعيدة
```bash
githydra remote add origin <url>  # إضافة مستودع بعيد
githydra sync push                # دفع التغييرات
githydra sync pull                # سحب التغييرات
```

#### المميزات المتقدمة
```bash
githydra stash save -m "عمل جاري" # حفظ مؤقت
githydra tag create v1.0          # إنشاء وسم
githydra bisect start             # بدء البحث الثنائي
githydra blame src/main.py        # عرض المؤلف
githydra archive create --format zip  # إنشاء أرشيف
```

#### الإحصائيات والتحليلات
```bash
githydra statistics overview      # إحصائيات المستودع
githydra statistics contributors  # إحصائيات المساهمين
githydra statistics activity      # تحليل النشاط
```

### 🎨 المميزات البارزة

- **واجهة جميلة**: واجهة طرفية غنية بالألوان والجداول وأشرطة التقدم
- **قوائم تفاعلية**: تنقل سهل عبر جميع المميزات
- **تسجيل شامل**: جميع العمليات مسجلة في `~/.githydra/logs/`
- **معالجة ذكية للأخطاء**: رسائل خطأ واضحة واستعادة تلقائية
- **التكوين**: قابل للتخصيص عبر `~/.githydra/config.yaml`
- **الاختصارات**: إنشاء اختصارات للأوامر المتكررة
- **تتبع التقدم**: ملاحظات مرئية للعمليات الطويلة
- **تكامل Git**: خلفية GitPython سلسة

### 🔧 التكوين

يخزن GitHydra التكوين في `~/.githydra/`:
- `config.yaml` - تفضيلات المستخدم
- `aliases.yaml` - اختصارات الأوامر
- `logs/` - سجلات العمليات حسب التاريخ

### 👨‍💻 Developer / المطور

**Name / الاسم:** Abdulaziz Alqudimi  
**Email / البريد الإلكتروني:** eng7mi@gmail.com  
**Repository / المستودع:** https://github.com/Alqudimi/GitHydra

### 🤝 Contributing / المساهمة

Contributions are welcome! Feel free to submit issues or pull requests.

المساهمات مرحب بها! لا تتردد في إرسال المشاكل أو طلبات السحب.

### 📧 Contact / التواصل

For questions, suggestions, or support:
- **Email:** eng7mi@gmail.com
- **GitHub Issues:** https://github.com/Alqudimi/GitHydra/issues

للأسئلة أو الاقتراحات أو الدعم:
- **البريد الإلكتروني:** eng7mi@gmail.com
- **مشاكل GitHub:** https://github.com/Alqudimi/GitHydra/issues

### 📄 License / الترخيص

MIT License - Free to use and modify.

ترخيص MIT - يمكنك الاستخدام والتعديل بحرية.

### 🐛 Bug Reports / الإبلاغ عن الأخطاء

Found a bug? Please open an issue with:
- GitHydra version / إصدار GitHydra
- Python version / إصدار Python
- Error message / رسالة الخطأ
- Steps to reproduce / خطوات إعادة الإنتاج

---

<div align="center">

**Made with ❤️ by Abdulaziz Alqudimi**

**صُنع بـ ❤️ من عبدالعزيز القديمي**

[GitHub](https://github.com/Alqudimi/GitHydra) | [Email](mailto:eng7mi@gmail.com)

</div>
