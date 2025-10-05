"""Interactive staging commands"""

import click
import questionary
from src.ui.console import console, print_success, print_error, print_info, print_diff
from src.utils.git_helper import get_repo, get_modified_files, get_untracked_files, get_staged_files
from src.logger import log_command

@click.group('stage')
def stage_cmd():
    """Interactive staging area management"""
    pass

@stage_cmd.command('add')
@click.argument('files', nargs=-1)
@click.option('--all', '-a', is_flag=True, help='Stage all changes')
@click.option('--interactive', '-i', is_flag=True, help='Interactive file selection')
def add_files(files, all, interactive):
    """Add files to staging area"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if all:
            repo.git.add(A=True)
            print_success("Staged all changes")
            log_command('stage add', True, "All changes staged")
            return
        
        if interactive:
            modified = get_modified_files(repo)
            untracked = get_untracked_files(repo)
            all_files = modified + untracked
            
            if not all_files:
                print_info("No files to stage")
                return
            
            selected = questionary.checkbox(
                "Select files to stage:",
                choices=all_files
            ).ask()
            
            if selected:
                for file in selected:
                    repo.index.add([file])
                print_success(f"Staged {len(selected)} file(s)")
                log_command('stage add', True, f"Staged {len(selected)} files")
            else:
                print_info("No files selected")
        elif files:
            for file in files:
                repo.index.add([file])
            print_success(f"Staged {len(files)} file(s)")
            log_command('stage add', True, f"Staged {len(files)} files")
        else:
            print_error("No files specified. Use --all, --interactive, or provide file names")
        
    except Exception as e:
        print_error(f"Failed to stage files: {str(e)}")
        log_command('stage add', False, str(e))

@stage_cmd.command('remove')
@click.argument('files', nargs=-1)
@click.option('--all', '-a', is_flag=True, help='Unstage all changes')
def remove_files(files, all):
    """Remove files from staging area"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if all:
            repo.index.reset()
            print_success("Unstaged all changes")
            log_command('stage remove', True, "All changes unstaged")
        elif files:
            for file in files:
                repo.index.reset(paths=[file])
            print_success(f"Unstaged {len(files)} file(s)")
            log_command('stage remove', True, f"Unstaged {len(files)} files")
        else:
            print_error("No files specified. Use --all or provide file names")
        
    except Exception as e:
        print_error(f"Failed to unstage files: {str(e)}")
        log_command('stage remove', False, str(e))

@stage_cmd.command('diff')
@click.argument('file', required=False)
@click.option('--cached', is_flag=True, help='Show staged changes')
def show_diff(file, cached):
    """Show diff of changes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if cached:
            diff = repo.git.diff('--cached', file) if file else repo.git.diff('--cached')
        else:
            diff = repo.git.diff(file) if file else repo.git.diff()
        
        if diff:
            print_diff(diff)
        else:
            print_info("No changes to show")
        
        log_command('stage diff', True)
        
    except Exception as e:
        print_error(f"Failed to show diff: {str(e)}")
        log_command('stage diff', False, str(e))
