"""Branch management commands"""

import click
from src.ui.console import console, print_success, print_error, create_tree
from src.utils.git_helper import get_repo, get_branch_list
from src.logger import log_command

@click.group('branch')
def branch_cmd():
    """Branch management commands"""
    pass

@branch_cmd.command('list')
@click.option('--all', '-a', is_flag=True, help='List all branches including remotes')
def list_branches(all):
    """List all branches"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        branches = get_branch_list(repo)
        
        if not branches:
            print_error("No branches yet. Create your first commit to establish a branch.")
            return
        
        tree = create_tree("[bold cyan]Branches[/bold cyan]")
        
        for branch_name, is_current in branches:
            if is_current:
                tree.add(f"[bold green]* {branch_name}[/bold green]")
            else:
                tree.add(f"  {branch_name}")
        
        if all:
            for remote in repo.remotes:
                remote_tree = tree.add(f"[bold yellow]remotes/{remote.name}[/bold yellow]")
                for ref in remote.refs:
                    remote_tree.add(f"  {ref.name.split('/')[-1]}")
        
        console.print(tree)
        log_command('branch list', True)
        
    except Exception as e:
        print_error(f"Failed to list branches: {str(e)}")
        log_command('branch list', False, str(e))

@branch_cmd.command('create')
@click.argument('branch_name')
@click.option('--checkout', '-c', is_flag=True, help='Checkout the branch after creating')
def create_branch(branch_name, checkout):
    """Create a new branch"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        new_branch = repo.create_head(branch_name)
        print_success(f"Created branch '{branch_name}'")
        
        if checkout:
            repo.heads[branch_name].checkout()
            print_success(f"Switched to branch '{branch_name}'")
        
        log_command('branch create', True, f"Branch '{branch_name}' created")
        
    except Exception as e:
        print_error(f"Failed to create branch: {str(e)}")
        log_command('branch create', False, str(e))

@branch_cmd.command('switch')
@click.argument('branch_name')
def switch_branch(branch_name):
    """Switch to a different branch"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.heads[branch_name].checkout()
        print_success(f"Switched to branch '{branch_name}'")
        log_command('branch switch', True, f"Switched to '{branch_name}'")
        
    except Exception as e:
        print_error(f"Failed to switch branch: {str(e)}")
        log_command('branch switch', False, str(e))

@branch_cmd.command('delete')
@click.argument('branch_name')
@click.option('--force', '-f', is_flag=True, help='Force delete the branch')
def delete_branch(branch_name, force):
    """Delete a branch"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if force:
            repo.delete_head(branch_name, force=True)
        else:
            repo.delete_head(branch_name)
        
        print_success(f"Deleted branch '{branch_name}'")
        log_command('branch delete', True, f"Branch '{branch_name}' deleted")
        
    except Exception as e:
        print_error(f"Failed to delete branch: {str(e)}")
        log_command('branch delete', False, str(e))

@branch_cmd.command('merge')
@click.argument('branch_name')
@click.option('--no-ff', is_flag=True, help='Create a merge commit even if fast-forward is possible')
def merge_branch(branch_name, no_ff):
    """Merge a branch into the current branch"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        current = repo.active_branch.name
        base = repo.heads[branch_name]
        
        repo.git.merge(branch_name, no_ff=no_ff)
        
        print_success(f"Merged '{branch_name}' into '{current}'")
        log_command('branch merge', True, f"Merged '{branch_name}' into '{current}'")
        
    except Exception as e:
        print_error(f"Failed to merge branch: {str(e)}")
        log_command('branch merge', False, str(e))
