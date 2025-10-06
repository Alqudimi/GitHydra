"""Submodule management commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from src.utils.git_helper import get_repo
from src.logger import log_command
import questionary

@click.group('submodule')
def submodule_cmd():
    """Submodule management operations"""
    pass

@submodule_cmd.command('add')
@click.argument('url')
@click.argument('path', required=False)
@click.option('--branch', '-b', help='Branch to track')
@click.option('--name', help='Name for the submodule')
def add_submodule(url, path, branch, name):
    """Add a new submodule to the repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not path:
            path = url.split('/')[-1].replace('.git', '')
        
        args = ['add']
        
        if name:
            args.extend(['--name', name])
        
        if branch:
            args.extend(['-b', branch])
        
        args.extend([url, path])
        
        repo.git.submodule(*args)
        
        print_success(f"Added submodule '{path}' from {url}")
        
        panel_content = f"[bold cyan]URL:[/bold cyan] {url}\n"
        panel_content += f"[bold cyan]Path:[/bold cyan] {path}\n"
        if branch:
            panel_content += f"[bold cyan]Branch:[/bold cyan] {branch}"
        
        console.print(create_panel(panel_content, "Submodule Added"))
        log_command('submodule add', True, f"Added submodule at {path}")
        
    except Exception as e:
        print_error(f"Failed to add submodule: {str(e)}")
        log_command('submodule add', False, str(e))

@submodule_cmd.command('init')
@click.argument('paths', nargs=-1)
def init_submodule(paths):
    """Initialize submodules"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if paths:
            repo.git.submodule('init', *paths)
            print_success(f"Initialized {len(paths)} submodule(s)")
        else:
            repo.git.submodule('init')
            print_success("Initialized all submodules")
        
        log_command('submodule init', True)
        
    except Exception as e:
        print_error(f"Failed to initialize submodules: {str(e)}")
        log_command('submodule init', False, str(e))

@submodule_cmd.command('update')
@click.option('--init', is_flag=True, help='Initialize submodules before updating')
@click.option('--recursive', '-r', is_flag=True, help='Update recursively')
@click.option('--remote', is_flag=True, help='Update to latest remote commit')
def update_submodule(init, recursive, remote):
    """Update submodules"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['update']
        if init:
            args.append('--init')
        if recursive:
            args.append('--recursive')
        if remote:
            args.append('--remote')
        
        repo.git.submodule(*args)
        print_success("Updated submodules successfully")
        log_command('submodule update', True)
        
    except Exception as e:
        print_error(f"Failed to update submodules: {str(e)}")
        log_command('submodule update', False, str(e))

@submodule_cmd.command('status')
@click.option('--recursive', '-r', is_flag=True, help='Show status recursively')
def status_submodule(recursive):
    """Show submodule status"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['status']
        if recursive:
            args.append('--recursive')
        
        output = repo.git.submodule(*args)
        
        if not output:
            print_info("No submodules found")
            return
        
        lines = output.strip().split('\n')
        table = create_table("Submodules Status", ["Status", "Commit", "Path"])
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                status = parts[0][0] if parts[0] else ' '
                commit = parts[0][1:8] if len(parts[0]) > 1 else parts[1][:7]
                path = parts[1] if len(parts) > 1 else ''
                
                status_symbol = {
                    '-': '[yellow]Not initialized[/yellow]',
                    '+': '[green]Updated[/green]',
                    'U': '[red]Merge conflict[/red]'
                }.get(status, '[cyan]Current[/cyan]')
                
                table.add_row(status_symbol, commit, path)
        
        console.print(table)
        log_command('submodule status', True)
        
    except Exception as e:
        print_error(f"Failed to show submodule status: {str(e)}")
        log_command('submodule status', False, str(e))

@submodule_cmd.command('sync')
@click.option('--recursive', '-r', is_flag=True, help='Sync recursively')
def sync_submodule(recursive):
    """Sync submodule URLs"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['sync']
        if recursive:
            args.append('--recursive')
        
        repo.git.submodule(*args)
        print_success("Synced submodule URLs successfully")
        log_command('submodule sync', True)
        
    except Exception as e:
        print_error(f"Failed to sync submodules: {str(e)}")
        log_command('submodule sync', False, str(e))

@submodule_cmd.command('foreach')
@click.argument('command', required=True)
@click.option('--recursive', '-r', is_flag=True, help='Execute recursively')
def foreach_submodule(command, recursive):
    """Execute a command in each submodule"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['foreach']
        if recursive:
            args.append('--recursive')
        args.append(command)
        
        output = repo.git.submodule(*args)
        console.print(output)
        print_success(f"Executed command in all submodules")
        log_command('submodule foreach', True, f"Command: {command}")
        
    except Exception as e:
        print_error(f"Failed to execute command: {str(e)}")
        log_command('submodule foreach', False, str(e))

@submodule_cmd.command('deinit')
@click.argument('paths', nargs=-1, required=True)
@click.option('--force', '-f', is_flag=True, help='Force deinitialization')
def deinit_submodule(paths, force):
    """Deinitialize submodules"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['deinit']
        if force:
            args.append('--force')
        args.extend(paths)
        
        repo.git.submodule(*args)
        print_success(f"Deinitialized {len(paths)} submodule(s)")
        log_command('submodule deinit', True)
        
    except Exception as e:
        print_error(f"Failed to deinitialize submodules: {str(e)}")
        log_command('submodule deinit', False, str(e))
