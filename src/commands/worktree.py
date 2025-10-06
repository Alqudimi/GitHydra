"""Worktree management commands"""

import click
from pathlib import Path
from src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.group('worktree')
def worktree_cmd():
    """Worktree management operations"""
    pass

@worktree_cmd.command('add')
@click.argument('path')
@click.argument('branch', required=False)
@click.option('--new-branch', '-b', help='Create and checkout a new branch')
@click.option('--detach', is_flag=True, help='Detach HEAD at named commit')
@click.option('--force', '-f', is_flag=True, help='Force creation even if path exists')
def add_worktree(path, branch, new_branch, detach, force):
    """Add a new worktree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['add']
        
        if force:
            args.append('--force')
        
        if detach:
            args.append('--detach')
        
        if new_branch:
            args.extend(['-b', new_branch])
        
        args.append(path)
        
        if branch and not new_branch:
            args.append(branch)
        
        repo.git.worktree(*args)
        
        print_success(f"Created worktree at '{path}'")
        
        panel_content = f"[bold cyan]Path:[/bold cyan] {path}\n"
        if new_branch:
            panel_content += f"[bold cyan]New Branch:[/bold cyan] {new_branch}"
        elif branch:
            panel_content += f"[bold cyan]Branch:[/bold cyan] {branch}"
        else:
            panel_content += f"[bold cyan]Mode:[/bold cyan] Detached HEAD"
        
        console.print(create_panel(panel_content, "Worktree Created"))
        log_command('worktree add', True, f"Added worktree at {path}")
        
    except Exception as e:
        print_error(f"Failed to add worktree: {str(e)}")
        log_command('worktree add', False, str(e))

@worktree_cmd.command('list')
@click.option('--porcelain', is_flag=True, help='Machine-readable output')
def list_worktrees(porcelain):
    """List all worktrees"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if porcelain:
            output = repo.git.worktree('list', '--porcelain')
            console.print(output)
        else:
            output = repo.git.worktree('list')
            lines = output.strip().split('\n')
            
            if not lines or not lines[0]:
                print_info("No worktrees found")
                return
            
            table = create_table("Worktrees", ["Path", "Branch", "Commit"])
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    path = parts[0]
                    commit = parts[1] if len(parts) > 1 else ''
                    branch = parts[2].strip('[]') if len(parts) > 2 else 'detached'
                    
                    is_main = '(bare)' not in line and path == repo.working_dir
                    path_display = f"[bold green]{path}[/bold green]" if is_main else path
                    
                    table.add_row(path_display, branch, commit[:7] if commit else '')
            
            console.print(table)
        
        log_command('worktree list', True)
        
    except Exception as e:
        print_error(f"Failed to list worktrees: {str(e)}")
        log_command('worktree list', False, str(e))

@worktree_cmd.command('remove')
@click.argument('path')
@click.option('--force', '-f', is_flag=True, help='Force removal even with uncommitted changes')
def remove_worktree(path, force):
    """Remove a worktree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['remove']
        if force:
            args.append('--force')
        args.append(path)
        
        repo.git.worktree(*args)
        print_success(f"Removed worktree '{path}'")
        log_command('worktree remove', True, f"Removed worktree at {path}")
        
    except Exception as e:
        print_error(f"Failed to remove worktree: {str(e)}")
        log_command('worktree remove', False, str(e))

@worktree_cmd.command('prune')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be pruned')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def prune_worktrees(dry_run, verbose):
    """Prune worktree information"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['prune']
        if dry_run:
            args.append('--dry-run')
        if verbose:
            args.append('--verbose')
        
        output = repo.git.worktree(*args)
        
        if output:
            console.print(output)
            print_success("Pruned stale worktree information")
        else:
            print_info("No stale worktrees to prune")
        
        log_command('worktree prune', True)
        
    except Exception as e:
        print_error(f"Failed to prune worktrees: {str(e)}")
        log_command('worktree prune', False, str(e))

@worktree_cmd.command('lock')
@click.argument('path')
@click.option('--reason', help='Reason for locking')
def lock_worktree(path, reason):
    """Lock a worktree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['lock']
        if reason:
            args.extend(['--reason', reason])
        args.append(path)
        
        repo.git.worktree(*args)
        print_success(f"Locked worktree '{path}'")
        log_command('worktree lock', True, f"Locked worktree at {path}")
        
    except Exception as e:
        print_error(f"Failed to lock worktree: {str(e)}")
        log_command('worktree lock', False, str(e))

@worktree_cmd.command('unlock')
@click.argument('path')
def unlock_worktree(path):
    """Unlock a worktree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.worktree('unlock', path)
        print_success(f"Unlocked worktree '{path}'")
        log_command('worktree unlock', True, f"Unlocked worktree at {path}")
        
    except Exception as e:
        print_error(f"Failed to unlock worktree: {str(e)}")
        log_command('worktree unlock', False, str(e))

@worktree_cmd.command('move')
@click.argument('source')
@click.argument('destination')
def move_worktree(source, destination):
    """Move a worktree to a new location"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.worktree('move', source, destination)
        print_success(f"Moved worktree from '{source}' to '{destination}'")
        log_command('worktree move', True, f"Moved worktree from {source} to {destination}")
        
    except Exception as e:
        print_error(f"Failed to move worktree: {str(e)}")
        log_command('worktree move', False, str(e))
