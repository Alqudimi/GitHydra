# GitHydra - Comprehensive Git Automation CLI Tool

## Overview
GitHydra is a powerful Python-based command-line tool that provides a beautiful, intuitive interface for managing all Git operations. Built with Rich for stunning terminal UI, Click for robust CLI framework, and GitPython for Git integration.

## Recent Changes
- **2025-10-05**: Version 2.0 - Major Feature Update
  - **Interactive Menu Interface**: Added menu-driven interface with numbered options for easy navigation
  - **Repository Repair Tools**: fsck, gc, prune, index repair, and repository info commands
  - **Stash Management**: Full stash support (save, list, apply, pop, drop, clear)
  - **Tag Management**: Create, list, delete, and show tags with full annotation support
  - **Advanced Operations**: reset (soft/mixed/hard), revert, cherry-pick, and enhanced diff
  - All new features tested and working correctly
  
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
  │   └── alias.py       # Command aliases
  ├── ui/
  │   └── console.py     # Rich UI components (panels, tables, trees, progress bars)
  ├── utils/
  │   └── git_helper.py  # Git utility functions (repo access, file operations)
  └── logger.py          # Logging system with file and console output
```

### Key Features
1. **Interactive Menu Interface**: Menu-driven interface with numbered options for easy navigation
2. **Beautiful Terminal UI**: Rich library integration with colorized output, tables, panels, and progress indicators
3. **Complete Git Coverage**: All essential Git commands with enhanced functionality
4. **Repository Maintenance**: Integrity checks, optimization, and repair tools
5. **Advanced Operations**: Stash management, tagging, reset, revert, cherry-pick
6. **Interactive Experience**: Smart prompts, file selection, and visual diffs using Questionary
7. **Professional Logging**: Comprehensive operation tracking saved to ~/.githydra/logs/
8. **Configuration Management**: User preferences and Git settings via YAML
9. **Smart Aliases**: Pre-configured and customizable command shortcuts
10. **Error Resilience**: Handles edge cases like fresh repositories without HEAD
11. **Modular Architecture**: Clean separation of concerns for easy maintenance and extension

### Usage
Run GitHydra from the terminal:

**Interactive Mode (Recommended for beginners):**
```bash
python githydra.py interactive
```

**Command Line Mode:**
```bash
python githydra.py --help
python githydra.py init [path]
python githydra.py status
python githydra.py stage add --interactive
python githydra.py commit -m "message"
python githydra.py branch list
python githydra.py log --graph
python githydra.py sync push
python githydra.py stash save -m "message"
python githydra.py tag create v1.0
python githydra.py repair info
python githydra.py diff --cached
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
