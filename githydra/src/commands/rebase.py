"""Interactive rebase and advanced rebase operations"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command
import questionary

@click.group('rebase')
def rebase_cmd():
    """Rebase operations"""
    pass

@rebase_cmd.command('start')
@click.argument('upstream')
@click.option('--interactive', '-i', is_flag=True, help='Interactive rebase')
@click.option('--onto', help='Rebase onto a different branch')
@click.option('--autosquash', is_flag=True, help='Automatically squash commits')
@click.option('--autostash', is_flag=True, help='Automatically stash and unstash')
def start_rebase(upstream, interactive, onto, autosquash, autostash):
    """Start a rebase operation (upstream is required)"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = []
        
        if interactive:
            args.append('-i')
        
        if autosquash:
            args.append('--autosquash')
        
        if autostash:
            args.append('--autostash')
        
        if onto:
            args.extend(['--onto', onto])
        
        args.append(upstream)
        
        output = repo.git.rebase(*args)
        if output:
            console.print(output)
        
        target = onto if onto else upstream
        print_success(f"Rebase started onto {target}")
        
        log_command('rebase start', True, f"Rebased onto {target}")
        
    except Exception as e:
        print_error(f"Failed to start rebase: {str(e)}")
        log_command('rebase start', False, str(e))

@rebase_cmd.command('continue')
def continue_rebase():
    """Continue rebase after resolving conflicts"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.rebase('--continue')
        console.print(output)
        print_success("Rebase continued")
        log_command('rebase continue', True)
        
    except Exception as e:
        print_error(f"Failed to continue rebase: {str(e)}")
        log_command('rebase continue', False, str(e))

@rebase_cmd.command('skip')
def skip_rebase():
    """Skip current commit and continue rebase"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.rebase('--skip')
        console.print(output)
        print_success("Skipped commit")
        log_command('rebase skip', True)
        
    except Exception as e:
        print_error(f"Failed to skip commit: {str(e)}")
        log_command('rebase skip', False, str(e))

@rebase_cmd.command('abort')
def abort_rebase():
    """Abort rebase and return to original state"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        confirm = questionary.confirm(
            "Are you sure you want to abort the rebase?",
            default=False
        ).ask()
        
        if not confirm:
            print_info("Abort cancelled")
            return
        
        repo.git.rebase('--abort')
        print_success("Rebase aborted")
        log_command('rebase abort', True)
        
    except Exception as e:
        print_error(f"Failed to abort rebase: {str(e)}")
        log_command('rebase abort', False, str(e))

@rebase_cmd.command('edit-todo')
def edit_todo():
    """Edit the rebase todo list"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.rebase('--edit-todo')
        print_success("Todo list opened for editing")
        log_command('rebase edit-todo', True)
        
    except Exception as e:
        print_error(f"Failed to edit todo: {str(e)}")
        log_command('rebase edit-todo', False, str(e))

@rebase_cmd.command('squash')
@click.argument('commits', type=int, default=2)
def squash_commits(commits):
    """Interactively squash last N commits"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if commits < 2:
            print_error("Need at least 2 commits to squash")
            return
        
        repo.git.rebase('-i', f'HEAD~{commits}')
        print_info(f"Interactive rebase started for last {commits} commits")
        print_info("Change 'pick' to 'squash' or 's' for commits you want to squash")
        
        log_command('rebase squash', True, f"Squashing {commits} commits")
        
    except Exception as e:
        print_error(f"Failed to start squash: {str(e)}")
        log_command('rebase squash', False, str(e))
