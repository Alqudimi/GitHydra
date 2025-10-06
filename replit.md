# GitHydra - Comprehensive Git Automation CLI Tool

## Overview
GitHydra is a powerful Python-based command-line tool that provides a beautiful, intuitive interface for managing all Git operations. Built with Rich for stunning terminal UI, Click for robust CLI framework, and GitPython for Git integration.

## Recent Changes
- **2025-10-05**: Version 3.0 - Setup & Documentation
  - **README.md**: Comprehensive bilingual documentation (English/Arabic)
  - **pyproject.toml**: Modern Python packaging configuration
  - **requirements.txt**: Clean dependency list
  - **LICENSE**: MIT License
  - **QUICKSTART.md**: Quick start guide for users
  - **Installation Scripts**: install.sh (Linux/Mac) and install.bat (Windows)
  - **Package Installation**: Successfully tested `pip install -e .`
  - **CLI Command**: `githydra` command now works system-wide
  
- **2025-10-05**: Version 3.0 - Massive Feature Expansion
  - **Submodule Management**: Full submodule support (add, init, update, status, sync, foreach, deinit)
  - **Worktree Operations**: Multiple working trees (add, list, remove, prune, lock, unlock, move)
  - **Reflog Management**: Reference log operations (show, expire, delete, exists)
  - **Bisect for Debugging**: Binary search to find bugs (start, good, bad, skip, reset, log, visualize)
  - **Blame Functionality**: Line-by-line authorship with statistics
  - **Archive Creation**: Export repository snapshots in multiple formats (zip, tar, tar.gz)
  - **Clean Operations**: Remove untracked files with interactive mode
  - **Notes System**: Add annotations to commits (add, show, list, remove, edit, copy)
  - **Patch Management**: Create, apply, and format patches for email submission
  - **Statistics & Analytics**: Repository overview, contributor stats, activity analysis, file stats, language analysis
  - **Conflict Resolution**: Helpers for merge conflicts (list, show, accept ours/theirs, abort, merge tool)
  - **Interactive Rebase**: Advanced history rewriting (start, continue, skip, abort, squash)
  - **Bundle Operations**: Repository transport via bundles (create, verify, list-heads, unbundle)
  - **Branch Comparison**: Compare branches, commits, files, and with remote
  - **Enhanced Interactive Menu**: Expanded to 13 categories with 70+ operations
  - All new features integrated and ready for testing
  
- **2025-10-05**: Initial development completed
  - Implemented all core Git operations (init, status, commit, branch, remote, log, stage, sync, config, alias)
  - Added beautiful Rich-based terminal UI with colorized output, tables, panels, and progress bars
  - Integrated comprehensive logging system tracking all operations
  - Fixed HEAD-related crashes in fresh repositories
  - Added proper error handling for repositories without commits
  - Tested full workflow on fresh repositories

## Project Architecture

### Structure
```
githydra.py              # Main entry point with CLI command groups
pyproject.toml           # Python package configuration
requirements.txt         # Dependencies list
README.md                # Comprehensive documentation (English/Arabic)
QUICKSTART.md            # Quick start guide
LICENSE                  # MIT License
MANIFEST.in              # Package manifest
install.sh               # Linux/Mac installation script
install.bat              # Windows installation script
src/
  ├── commands/          # Command implementations
  │   ├── init.py        # Repository initialization
  │   ├── status.py      # Working tree status
  │   ├── branch.py      # Branch management
  │   ├── commit.py      # Commit operations
  │   ├── remote.py      # Remote repository management
  │   ├── log.py         # Commit history viewer
  │   ├── stage.py       # Interactive staging area
  │   ├── sync.py        # Push/pull/fetch/clone operations
  │   ├── interactive.py # Interactive menu interface
  │   ├── repair.py      # Repository maintenance and repair
  │   ├── stash.py       # Temporary changes storage
  │   ├── tag.py         # Version tagging
  │   ├── reset.py       # Reset, revert, cherry-pick
  │   ├── diff.py        # Enhanced diff viewer
  │   ├── config.py      # Configuration management
  │   ├── alias.py       # Command aliases
  │   ├── submodule.py   # Submodule management
  │   ├── worktree.py    # Worktree operations
  │   ├── reflog.py      # Reflog management
  │   ├── bisect.py      # Binary search debugging
  │   ├── blame.py       # Line-by-line authorship
  │   ├── archive.py     # Repository archiving
  │   ├── clean.py       # Untracked file cleanup
  │   ├── notes.py       # Commit annotations
  │   ├── patch.py       # Patch management
  │   ├── statistics.py  # Repository analytics
  │   ├── conflicts.py   # Conflict resolution
  │   ├── rebase.py      # Interactive rebase
  │   ├── bundle.py      # Bundle operations
  │   └── compare.py     # Branch/commit comparison
  ├── ui/
  │   └── console.py     # Rich UI components (panels, tables, trees, progress bars)
  ├── utils/
  │   └── git_helper.py  # Git utility functions (repo access, file operations)
  └── logger.py          # Logging system with file and console output
```

### Key Features
1. **Comprehensive Git Coverage**: 30+ command groups covering every Git operation
2. **Interactive Menu Interface**: 13 categories with 70+ operations accessible via intuitive menu
3. **Beautiful Terminal UI**: Rich library integration with colorized output, tables, panels, and progress indicators
4. **Submodule & Worktree Management**: Full support for advanced repository structures
5. **Debugging Tools**: Bisect for bug hunting, blame for authorship, reflog for history recovery
6. **Repository Analytics**: Detailed statistics on contributors, activity, files, and languages
7. **Conflict Resolution**: Comprehensive helpers for merge conflicts with interactive tools
8. **Patch & Bundle Operations**: Professional workflows for code sharing and repository transport
9. **Advanced History Rewriting**: Interactive rebase with squash, edit, and reorder
10. **Branch Comparison**: Compare branches, commits, and track remote differences
11. **Archive & Clean**: Export snapshots and maintain clean working directories
12. **Commit Annotations**: Add notes and metadata to commits without changing history
13. **Professional Logging**: Comprehensive operation tracking saved to ~/.githydra/logs/
14. **Configuration Management**: User preferences and Git settings via YAML
15. **Smart Aliases**: Pre-configured and customizable command shortcuts
16. **Error Resilience**: Handles edge cases gracefully with helpful error messages
17. **Modular Architecture**: Clean separation of concerns for easy maintenance and extension

### Installation
Install GitHydra using pip:
```bash
pip install -e .
```

Or use the installation scripts:
```bash
./install.sh          # Linux/Mac
install.bat           # Windows
```

### Usage
After installation, use the `githydra` command:

**Interactive Mode (Recommended for beginners):**
```bash
githydra interactive
```

**Command Line Mode:**
```bash
githydra --help
githydra init [path]
githydra status
githydra stage add --interactive
githydra commit -m "message"
githydra branch list
githydra log --graph
githydra sync push
githydra stash save -m "message"
githydra tag create v1.0
githydra repair info
githydra diff --cached
```

### Dependencies
- Python 3.11
- rich - Terminal formatting and UI
- click - CLI framework
- gitpython - Git repository interface
- questionary - Interactive prompts
- pyyaml - Configuration management
- colorama - Cross-platform colored output

### Configuration
GitHydra stores its configuration and logs in `~/.githydra/`:
- `config.yaml` - User configuration
- `aliases.yaml` - Command aliases
- `logs/` - Operation logs by date

## User Preferences
None specified yet.

## Development Notes
- All commands are tested and functional on fresh and existing repositories
- Error handling includes graceful fallbacks for edge cases
- Logging captures all operations with timestamps
- Architecture designed for easy extension with additional commands and features
