"""Stash commands for temporary storage of changes"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_table
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command
import questionary

@click.group('stash')
def stash_cmd():
    """Stash changes temporarily"""
    pass

@stash_cmd.command('save')
@click.option('--message', '-m', help='Stash message')
@click.option('--include-untracked', '-u', is_flag=True, help='Include untracked files')
def save_stash(message, include_untracked):
    """Save current changes to stash"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not message:
            message = questionary.text("Enter stash message (optional):").ask()
        
        if include_untracked:
            if message:
                repo.git.stash('save', '-u', message)
            else:
                repo.git.stash('save', '-u')
        else:
            if message:
                repo.git.stash('save', message)
            else:
                repo.git.stash('save')
        
        print_success(f"Changes stashed successfully")
        log_command('stash save', True)
        
    except Exception as e:
        print_error(f"Failed to stash changes: {str(e)}")
        log_command('stash save', False, str(e))

@stash_cmd.command('list')
def list_stash():
    """List all stashes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        stashes = repo.git.stash('list').split('\n') if repo.git.stash('list') else []
        
        if not stashes or not stashes[0]:
            print_info("No stashes found")
            return
        
        table = create_table("Stashed Changes", ["Index", "Description"])
        
        for stash in stashes:
            if stash:
                parts = stash.split(':', 1)
                if len(parts) == 2:
                    table.add_row(parts[0], parts[1].strip())
        
        console.print(table)
        log_command('stash list', True)
        
    except Exception as e:
        print_error(f"Failed to list stashes: {str(e)}")
        log_command('stash list', False, str(e))

@stash_cmd.command('apply')
@click.argument('index', default='0')
def apply_stash(index):
    """Apply a stash"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.stash('apply', f'stash@{{{index}}}')
        print_success(f"Applied stash@{{{index}}}")
        log_command('stash apply', True)
        
    except Exception as e:
        print_error(f"Failed to apply stash: {str(e)}")
        log_command('stash apply', False, str(e))

@stash_cmd.command('pop')
@click.argument('index', default='0')
def pop_stash(index):
    """Apply and remove a stash"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.stash('pop', f'stash@{{{index}}}')
        print_success(f"Popped stash@{{{index}}}")
        log_command('stash pop', True)
        
    except Exception as e:
        print_error(f"Failed to pop stash: {str(e)}")
        log_command('stash pop', False, str(e))

@stash_cmd.command('drop')
@click.argument('index', default='0')
def drop_stash(index):
    """Delete a stash"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.stash('drop', f'stash@{{{index}}}')
        print_success(f"Dropped stash@{{{index}}}")
        log_command('stash drop', True)
        
    except Exception as e:
        print_error(f"Failed to drop stash: {str(e)}")
        log_command('stash drop', False, str(e))

@stash_cmd.command('clear')
def clear_stash():
    """Remove all stashes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        confirm = questionary.confirm("Are you sure you want to clear all stashes?").ask()
        
        if confirm:
            repo.git.stash('clear')
            print_success("All stashes cleared")
            log_command('stash clear', True)
        else:
            print_info("Operation cancelled")
        
    except Exception as e:
        print_error(f"Failed to clear stashes: {str(e)}")
        log_command('stash clear', False, str(e))
