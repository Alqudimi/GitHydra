"""Sync operations: push, pull, fetch, clone"""

import click
import git
from pathlib import Path
from src.ui.console import console, print_success, print_error, print_info, create_progress
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.group('sync')
def sync_cmd():
    """Synchronization operations"""
    pass

@sync_cmd.command('push')
@click.option('--remote', '-r', default='origin', help='Remote name')
@click.option('--branch', '-b', help='Branch name')
@click.option('--force', '-f', is_flag=True, help='Force push')
@click.option('--all', is_flag=True, help='Push all branches')
def push(remote, branch, force, all):
    """Push commits to remote repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not branch and not all:
            branch = repo.active_branch.name
        
        remote_obj = repo.remote(remote)
        
        with create_progress() as progress:
            task = progress.add_task(f"Pushing to {remote}...", total=100)
            
            if all:
                remote_obj.push(force=force)
                progress.update(task, completed=100)
                print_success(f"Pushed all branches to '{remote}'")
            else:
                remote_obj.push(branch, force=force)
                progress.update(task, completed=100)
                print_success(f"Pushed '{branch}' to '{remote}'")
        
        log_command('push', True, f"Pushed to {remote}")
        
    except Exception as e:
        print_error(f"Failed to push: {str(e)}")
        log_command('push', False, str(e))

@sync_cmd.command('pull')
@click.option('--remote', '-r', default='origin', help='Remote name')
@click.option('--branch', '-b', help='Branch name')
@click.option('--rebase', is_flag=True, help='Rebase instead of merge')
def pull(remote, branch, rebase):
    """Pull changes from remote repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not branch:
            branch = repo.active_branch.name
        
        remote_obj = repo.remote(remote)
        
        with create_progress() as progress:
            task = progress.add_task(f"Pulling from {remote}...", total=100)
            
            if rebase:
                remote_obj.pull(branch, rebase=True)
            else:
                remote_obj.pull(branch)
            
            progress.update(task, completed=100)
        
        print_success(f"Pulled '{branch}' from '{remote}'")
        log_command('pull', True, f"Pulled from {remote}")
        
    except Exception as e:
        print_error(f"Failed to pull: {str(e)}")
        log_command('pull', False, str(e))

@sync_cmd.command('fetch')
@click.option('--remote', '-r', default='origin', help='Remote name')
@click.option('--all', is_flag=True, help='Fetch from all remotes')
def fetch(remote, all):
    """Fetch changes from remote repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        with create_progress() as progress:
            task = progress.add_task("Fetching...", total=100)
            
            if all:
                for r in repo.remotes:
                    r.fetch()
                progress.update(task, completed=100)
                print_success("Fetched from all remotes")
            else:
                remote_obj = repo.remote(remote)
                remote_obj.fetch()
                progress.update(task, completed=100)
                print_success(f"Fetched from '{remote}'")
        
        log_command('fetch', True)
        
    except Exception as e:
        print_error(f"Failed to fetch: {str(e)}")
        log_command('fetch', False, str(e))

@sync_cmd.command('clone')
@click.argument('url')
@click.argument('path', default='.', type=click.Path())
@click.option('--branch', '-b', help='Clone specific branch')
@click.option('--depth', type=int, help='Create a shallow clone with specified depth')
def clone(url, path, branch, depth):
    """Clone a remote repository"""
    try:
        clone_path = Path(path).resolve()
        
        with create_progress() as progress:
            task = progress.add_task(f"Cloning {url}...", total=100)
            
            kwargs = {}
            if branch:
                kwargs['branch'] = branch
            if depth:
                kwargs['depth'] = depth
            
            repo = git.Repo.clone_from(url, clone_path, **kwargs)
            progress.update(task, completed=100)
        
        print_success(f"Cloned repository to {clone_path}")
        log_command('clone', True, f"Cloned {url}")
        
    except Exception as e:
        print_error(f"Failed to clone: {str(e)}")
        log_command('clone', False, str(e))
