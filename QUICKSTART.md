# GitHydra Quick Start Guide 🚀

## دليل البداية السريعة

---

## Installation / التثبيت

### Method 1: Using pip (Recommended / موصى به)
```bash
pip install -e .
```

### Method 2: Using installation scripts / باستخدام نصوص التثبيت

**Linux/Mac:**
```bash
./install.sh
```

**Windows:**
```batch
install.bat
```

---

## Quick Usage / الاستخدام السريع

### Interactive Mode (Easiest / الأسهل)
```bash
githydra interactive
```
This launches a beautiful menu where you can navigate through all features!

هذا يشغّل قائمة جميلة يمكنك التنقل فيها عبر جميع المميزات!

### Command Line Mode / وضع سطر الأوامر

#### Basic Commands / أوامر أساسية
```bash
githydra status                    # Check repository status / فحص حالة المستودع
githydra commit -m "My message"    # Create commit / إنشاء التزام
githydra branch list               # List branches / قائمة الفروع
githydra log --graph               # View history / عرض التاريخ
```

#### Advanced Commands / أوامر متقدمة
```bash
githydra stash save -m "WIP"       # Stash changes / حفظ مؤقت
githydra tag create v1.0           # Create tag / إنشاء وسم
githydra bisect start              # Find bugs / إيجاد الأخطاء
githydra blame src/main.py         # Show authorship / عرض المؤلف
```

#### Statistics / الإحصائيات
```bash
githydra stats overview            # Repository overview / نظرة عامة
githydra stats contributors        # Contributor stats / إحصائيات المساهمين
githydra stats activity            # Activity analysis / تحليل النشاط
```

#### Advanced Features / مميزات متقدمة
```bash
githydra submodule add <url>       # Add submodule / إضافة وحدة فرعية
githydra worktree add <path>       # Create worktree / إنشاء شجرة عمل
githydra archive create --format zip  # Create archive / إنشاء أرشيف
githydra compare branches main dev # Compare branches / مقارنة الفروع
```

---

## Getting Help / الحصول على المساعدة

```bash
githydra --help                    # General help / مساعدة عامة
githydra <command> --help          # Command-specific help / مساعدة خاصة بالأمر
```

---

## Feature Categories / فئات المميزات

1. **Repository Operations** - Init, status, clone / عمليات المستودع
2. **File & Staging** - Interactive staging / الملفات والتجهيز
3. **Commits & History** - Commit, log, search / الالتزامات والتاريخ
4. **Branches** - Create, switch, delete / الفروع
5. **Remote & Sync** - Push, pull, fetch / البعيد والمزامنة
6. **Advanced Operations** - Stash, tags, reset / العمليات المتقدمة
7. **Submodules & Worktrees** - Advanced repo management / إدارة متقدمة
8. **Debugging & Search** - Bisect, blame, reflog / التصحيح والبحث
9. **Patches & Bundles** - Code sharing / مشاركة الكود
10. **Conflicts & Merging** - Conflict resolution / حل التعارضات
11. **Statistics & Analysis** - Repo analytics / تحليلات المستودع
12. **Maintenance & Repair** - Cleanup, repair / الصيانة والإصلاح
13. **Configuration** - Settings, aliases / الإعدادات

---

## Tips / نصائح

✅ Use interactive mode if you're new to Git / استخدم الوضع التفاعلي إذا كنت جديداً على Git

✅ Create aliases for frequent commands / أنشئ اختصارات للأوامر المتكررة

✅ Check logs in `~/.githydra/logs/` for troubleshooting / راجع السجلات للمساعدة في حل المشاكل

✅ Use `--help` with any command to learn more / استخدم `--help` مع أي أمر لمعرفة المزيد

---

## Examples / أمثلة

### Daily Workflow / سير العمل اليومي
```bash
githydra status                    # Check what changed
githydra stage add --interactive   # Stage files interactively
githydra commit -m "Add feature"   # Commit changes
githydra sync push                 # Push to remote
```

### Creating a Feature Branch / إنشاء فرع للميزة
```bash
githydra branch create feature/new-feature
githydra branch switch feature/new-feature
# ... make changes ...
githydra commit -m "Implement feature"
githydra sync push
```

### Debugging / التصحيح
```bash
githydra bisect start              # Start bisect
githydra bisect bad                # Mark current as bad
githydra bisect good <commit>      # Mark known good commit
# GitHydra will help you find the problematic commit!
```

---

## Developer / المطور

**Name / الاسم:** Abdulaziz Alqudimi  
**Email / البريد الإلكتروني:** eng7mi@gmail.com  
**Repository / المستودع:** https://github.com/Alqudimi/GitHydra

## Support / الدعم

Need help? Contact us! / تحتاج مساعدة؟ تواصل معنا!

- **Email / البريد الإلكتروني:** eng7mi@gmail.com
- **GitHub Issues:** https://github.com/Alqudimi/GitHydra/issues

---

**Enjoy using GitHydra! 🎉**

**استمتع باستخدام GitHydra! 🎉**

**Made with ❤️ by Abdulaziz Alqudimi**
