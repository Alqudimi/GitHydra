"""Remote repository management"""

import click
from githydra.src.ui.console import console, print_success, print_error, create_table
from githydra.src.utils.git_helper import get_repo, get_remote_list
from githydra.src.logger import log_command

@click.group('remote')
def remote_cmd():
    """Remote repository management"""
    pass

@remote_cmd.command('list')
@click.option('--verbose', '-v', is_flag=True, help='Show URLs')
def list_remotes(verbose):
    """List all remotes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        remotes = get_remote_list(repo)
        
        if not remotes:
            print_error("No remotes configured")
            return
        
        if verbose:
            table = create_table("Remotes", ["Name", "URL"])
            for name, url in remotes:
                table.add_row(name, url)
            console.print(table)
        else:
            for name, _ in remotes:
                console.print(name)
        
        log_command('remote list', True)
        
    except Exception as e:
        print_error(f"Failed to list remotes: {str(e)}")
        log_command('remote list', False, str(e))

@remote_cmd.command('add')
@click.argument('name')
@click.argument('url')
def add_remote(name, url):
    """Add a new remote"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.create_remote(name, url)
        print_success(f"Added remote '{name}': {url}")
        log_command('remote add', True, f"Remote '{name}' added")
        
    except Exception as e:
        print_error(f"Failed to add remote: {str(e)}")
        log_command('remote add', False, str(e))

@remote_cmd.command('remove')
@click.argument('name')
def remove_remote(name):
    """Remove a remote"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.delete_remote(name)
        print_success(f"Removed remote '{name}'")
        log_command('remote remove', True, f"Remote '{name}' removed")
        
    except Exception as e:
        print_error(f"Failed to remove remote: {str(e)}")
        log_command('remote remove', False, str(e))

@remote_cmd.command('rename')
@click.argument('old_name')
@click.argument('new_name')
def rename_remote(old_name, new_name):
    """Rename a remote"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        remote = repo.remote(old_name)
        remote.rename(new_name)
        print_success(f"Renamed remote '{old_name}' to '{new_name}'")
        log_command('remote rename', True, f"Remote renamed from '{old_name}' to '{new_name}'")
        
    except Exception as e:
        print_error(f"Failed to rename remote: {str(e)}")
        log_command('remote rename', False, str(e))
