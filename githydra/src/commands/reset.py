"""Reset and revert commands"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_warning
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command
import questionary

@click.group('reset')
def reset_cmd():
    """Reset current HEAD to specified state"""
    pass

@reset_cmd.command('soft')
@click.argument('commit', default='HEAD~1')
def reset_soft(commit):
    """Reset to commit keeping changes staged"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.reset('--soft', commit)
        print_success(f"Reset to {commit} (soft) - changes kept in staging area")
        log_command('reset soft', True)
        
    except Exception as e:
        print_error(f"Reset failed: {str(e)}")
        log_command('reset soft', False, str(e))

@reset_cmd.command('mixed')
@click.argument('commit', default='HEAD~1')
def reset_mixed(commit):
    """Reset to commit keeping changes unstaged"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.reset('--mixed', commit)
        print_success(f"Reset to {commit} (mixed) - changes kept in working directory")
        log_command('reset mixed', True)
        
    except Exception as e:
        print_error(f"Reset failed: {str(e)}")
        log_command('reset mixed', False, str(e))

@reset_cmd.command('hard')
@click.argument('commit', default='HEAD~1')
def reset_hard(commit):
    """Reset to commit discarding all changes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        confirm = questionary.confirm(
            f"WARNING: This will discard all changes. Continue?"
        ).ask()
        
        if not confirm:
            print_warning("Operation cancelled")
            return
        
        repo.git.reset('--hard', commit)
        print_success(f"Reset to {commit} (hard) - all changes discarded")
        log_command('reset hard', True)
        
    except Exception as e:
        print_error(f"Reset failed: {str(e)}")
        log_command('reset hard', False, str(e))

@click.command('revert')
@click.argument('commit')
@click.option('--no-commit', is_flag=True, help='Revert without committing')
def revert_cmd(commit, no_commit):
    """Revert a commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if no_commit:
            repo.git.revert(commit, '--no-commit')
            print_success(f"Reverted {commit} without committing")
        else:
            repo.git.revert(commit)
            print_success(f"Reverted {commit}")
        
        log_command('revert', True)
        
    except Exception as e:
        print_error(f"Revert failed: {str(e)}")
        log_command('revert', False, str(e))

@click.command('cherry-pick')
@click.argument('commit')
@click.option('--no-commit', is_flag=True, help='Apply without committing')
def cherry_pick_cmd(commit, no_commit):
    """Apply changes from specific commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if no_commit:
            repo.git.cherry_pick(commit, '--no-commit')
            print_success(f"Cherry-picked {commit} without committing")
        else:
            repo.git.cherry_pick(commit)
            print_success(f"Cherry-picked {commit}")
        
        log_command('cherry-pick', True)
        
    except Exception as e:
        print_error(f"Cherry-pick failed: {str(e)}")
        log_command('cherry-pick', False, str(e))
