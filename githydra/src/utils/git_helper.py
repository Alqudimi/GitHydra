"""Git helper utilities using GitPython - Enhanced with comprehensive error handling"""

import git
from pathlib import Path
from typing import Optional, List, Tuple
from githydra.src.ui.console import print_error, print_warning, console

def get_repo(path: str = ".") -> Optional[git.Repo]:
    """
    Get git repository object with comprehensive error handling
    
    Args:
        path: Path to repository (default: current directory)
        
    Returns:
        Repository object or None if error occurs
    """
    try:
        repo = git.Repo(path, search_parent_directories=True)
        return repo
    except git.InvalidGitRepositoryError:
        print_error("Not a git repository. Use 'githydra init' to initialize one.")
        return None
    except git.NoSuchPathError:
        print_error(f"Path does not exist: {path}")
        return None
    except PermissionError:
        print_error(f"Permission denied accessing repository at: {path}")
        return None
    except Exception as e:
        print_error(f"Error accessing repository: {str(e)}")
        console.print_exception(show_locals=False)
        return None

def is_git_repo(path: str = ".") -> bool:
    """
    Check if path is a git repository
    
    Args:
        path: Path to check (default: current directory)
        
    Returns:
        True if valid git repository, False otherwise
    """
    try:
        git.Repo(path, search_parent_directories=True)
        return True
    except (git.InvalidGitRepositoryError, git.NoSuchPathError, PermissionError):
        return False
    except Exception:
        return False

def get_modified_files(repo: git.Repo) -> List[str]:
    """
    Get list of modified files with error handling
    
    Args:
        repo: Git repository object
        
    Returns:
        List of modified file paths
    """
    try:
        return [item.a_path for item in repo.index.diff(None) if item.a_path]
    except git.GitCommandError as e:
        print_warning(f"Git command error getting modified files: {str(e)}")
        return []
    except AttributeError as e:
        print_warning(f"Repository state error: {str(e)}")
        return []
    except Exception as e:
        print_warning(f"Unexpected error getting modified files: {str(e)}")
        return []

def get_untracked_files(repo: git.Repo) -> List[str]:
    """
    Get list of untracked files with error handling
    
    Args:
        repo: Git repository object
        
    Returns:
        List of untracked file paths
    """
    try:
        return repo.untracked_files
    except git.GitCommandError as e:
        print_warning(f"Git command error getting untracked files: {str(e)}")
        return []
    except Exception as e:
        print_warning(f"Unexpected error getting untracked files: {str(e)}")
        return []

def get_staged_files(repo: git.Repo) -> List[str]:
    """
    Get list of staged files with comprehensive error handling
    
    Args:
        repo: Git repository object
        
    Returns:
        List of staged file paths
    """
    try:
        return [item.a_path for item in repo.index.diff("HEAD") if item.a_path]
    except (git.GitCommandError, git.BadName):
        try:
            return [entry[0] for entry in repo.index.entries.keys()]
        except AttributeError:
            return []
        except Exception:
            return []
    except AttributeError as e:
        print_warning(f"Repository index error: {str(e)}")
        return []
    except Exception as e:
        print_warning(f"Unexpected error getting staged files: {str(e)}")
        return []

def get_branch_list(repo: git.Repo) -> List[Tuple[str, bool]]:
    """
    Get list of branches with current branch indicator
    
    Args:
        repo: Git repository object
        
    Returns:
        List of tuples (branch_name, is_current)
    """
    branches = []
    try:
        try:
            current_branch = repo.active_branch.name
        except TypeError:
            current_branch = None
        except git.GitCommandError:
            current_branch = None
        except Exception:
            current_branch = None
        
        for branch in repo.branches:
            branches.append((branch.name, branch.name == current_branch))
    except git.GitCommandError as e:
        print_warning(f"Error listing branches: {str(e)}")
    except Exception as e:
        print_warning(f"Unexpected error getting branch list: {str(e)}")
    
    return branches

def get_remote_list(repo: git.Repo) -> List[Tuple[str, str]]:
    """
    Get list of remotes with URLs
    
    Args:
        repo: Git repository object
        
    Returns:
        List of tuples (remote_name, remote_url)
    """
    remotes = []
    try:
        for remote in repo.remotes:
            try:
                url = list(remote.urls)[0] if remote.urls else ""
                remotes.append((remote.name, url))
            except IndexError:
                remotes.append((remote.name, ""))
            except Exception:
                remotes.append((remote.name, "unknown"))
    except git.GitCommandError as e:
        print_warning(f"Error getting remotes: {str(e)}")
    except Exception as e:
        print_warning(f"Unexpected error getting remote list: {str(e)}")
    
    return remotes

def get_commit_history(repo: git.Repo, max_count: int = 10) -> List[dict]:
    """
    Get commit history with error handling
    
    Args:
        repo: Git repository object
        max_count: Maximum number of commits to retrieve
        
    Returns:
        List of commit dictionaries
    """
    commits = []
    try:
        for commit in list(repo.iter_commits(max_count=max_count)):
            try:
                commits.append({
                    'hash': commit.hexsha[:7],
                    'author': commit.author.name,
                    'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    'message': commit.message.strip().split('\n')[0]
                })
            except AttributeError as e:
                print_warning(f"Error processing commit {commit.hexsha[:7]}: {str(e)}")
                continue
            except Exception as e:
                print_warning(f"Unexpected error processing commit: {str(e)}")
                continue
    except git.GitCommandError as e:
        print_warning(f"Git command error getting commit history: {str(e)}")
    except ValueError as e:
        print_warning(f"Invalid value in commit history: {str(e)}")
    except Exception as e:
        print_warning(f"Unexpected error getting commit history: {str(e)}")
    
    return commits

def safe_git_operation(operation, error_message: str = "Git operation failed", **kwargs):
    """
    Safely execute a git operation with comprehensive error handling
    
    Args:
        operation: Callable git operation
        error_message: Custom error message
        **kwargs: Arguments to pass to the operation
        
    Returns:
        Result of operation or None if failed
    """
    try:
        return operation(**kwargs)
    except git.GitCommandError as e:
        print_error(f"{error_message}: {str(e)}")
        return None
    except PermissionError as e:
        print_error(f"Permission denied: {str(e)}")
        return None
    except OSError as e:
        print_error(f"File system error: {str(e)}")
        return None
    except Exception as e:
        print_error(f"{error_message}: {str(e)}")
        console.print_exception(show_locals=False)
        return None

def validate_branch_name(branch_name: str) -> bool:
    """
    Validate branch name according to git rules
    
    Args:
        branch_name: Name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not branch_name:
        return False
    
    invalid_chars = ['..', '~', '^', ':', '?', '*', '[', '\\', ' ']
    
    for char in invalid_chars:
        if char in branch_name:
            return False
    
    if branch_name.startswith('/') or branch_name.endswith('/'):
        return False
    
    if branch_name.startswith('.') or branch_name.endswith('.'):
        return False
    
    return True

def validate_commit_message(message: str) -> Tuple[bool, str]:
    """
    Validate commit message
    
    Args:
        message: Commit message to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Commit message cannot be empty"
    
    if len(message.strip()) < 3:
        return False, "Commit message is too short (minimum 3 characters)"
    
    return True, ""
