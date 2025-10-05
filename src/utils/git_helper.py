"""Git helper utilities using GitPython"""

import git
from pathlib import Path
from typing import Optional, List, Tuple
from src.ui.console import print_error, print_warning

def get_repo(path: str = ".") -> Optional[git.Repo]:
    """Get git repository object"""
    try:
        repo = git.Repo(path, search_parent_directories=True)
        return repo
    except git.InvalidGitRepositoryError:
        print_error("Not a git repository. Use 'githydra init' to initialize one.")
        return None
    except Exception as e:
        print_error(f"Error accessing repository: {str(e)}")
        return None

def is_git_repo(path: str = ".") -> bool:
    """Check if path is a git repository"""
    try:
        git.Repo(path, search_parent_directories=True)
        return True
    except:
        return False

def get_modified_files(repo: git.Repo) -> List[str]:
    """Get list of modified files"""
    try:
        return [item.a_path for item in repo.index.diff(None) if item.a_path]
    except Exception as e:
        print_warning(f"Error getting modified files: {str(e)}")
        return []

def get_untracked_files(repo: git.Repo) -> List[str]:
    """Get list of untracked files"""
    try:
        return repo.untracked_files
    except Exception as e:
        print_warning(f"Error getting untracked files: {str(e)}")
        return []

def get_staged_files(repo: git.Repo) -> List[str]:
    """Get list of staged files"""
    try:
        return [item.a_path for item in repo.index.diff("HEAD") if item.a_path]
    except (git.GitCommandError, git.BadName):
        try:
            return [entry[0] for entry in repo.index.entries.keys()]
        except:
            return []
    except Exception as e:
        print_warning(f"Error getting staged files: {str(e)}")
        return []

def get_branch_list(repo: git.Repo) -> List[Tuple[str, bool]]:
    """Get list of branches with current branch indicator"""
    branches = []
    try:
        try:
            current_branch = repo.active_branch.name
        except:
            current_branch = None
        
        for branch in repo.branches:
            branches.append((branch.name, branch.name == current_branch))
    except Exception as e:
        pass
    return branches

def get_remote_list(repo: git.Repo) -> List[Tuple[str, str]]:
    """Get list of remotes with URLs"""
    remotes = []
    try:
        for remote in repo.remotes:
            remotes.append((remote.name, list(remote.urls)[0] if remote.urls else ""))
    except Exception as e:
        print_warning(f"Error getting remotes: {str(e)}")
    return remotes

def get_commit_history(repo: git.Repo, max_count: int = 10) -> List[dict]:
    """Get commit history"""
    commits = []
    try:
        for commit in list(repo.iter_commits(max_count=max_count)):
            commits.append({
                'hash': commit.hexsha[:7],
                'author': commit.author.name,
                'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'message': commit.message.strip().split('\n')[0]
            })
    except Exception as e:
        print_warning(f"Error getting commit history: {str(e)}")
    return commits
