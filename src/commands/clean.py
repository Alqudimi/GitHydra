"""Clean untracked files commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_panel
from src.utils.git_helper import get_repo
from src.logger import log_command
import questionary

@click.command('clean')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be removed')
@click.option('--force', '-f', is_flag=True, help='Force removal')
@click.option('--directories', '-d', is_flag=True, help='Remove untracked directories')
@click.option('--ignored', '-x', is_flag=True, help='Remove ignored files too')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def clean_cmd(dry_run, force, directories, ignored, interactive):
    """Remove untracked files from the working tree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if interactive:
            args = ['-i']
            if directories:
                args.append('-d')
            if ignored:
                args.append('-x')
            
            repo.git.clean(*args)
            print_success("Interactive clean completed")
            log_command('clean', True, "Interactive clean")
            return
        
        if dry_run:
            args = ['-n']
            if directories:
                args.append('-d')
            if ignored:
                args.append('-x')
            
            output = repo.git.clean(*args)
            
            if not output:
                print_info("No untracked files to remove")
                return
            
            console.print("[bold yellow]Files that would be removed:[/bold yellow]")
            console.print(output)
            
            log_command('clean', True, "Dry run completed")
            return
        
        if not force:
            confirm = questionary.confirm(
                "Are you sure you want to remove untracked files? This cannot be undone.",
                default=False
            ).ask()
            
            if not confirm:
                print_info("Clean operation cancelled")
                return
            
            force = True
        
        args = []
        if force:
            args.append('-f')
        if directories:
            args.append('-d')
        if ignored:
            args.append('-x')
        
        output = repo.git.clean(*args)
        
        if output:
            console.print("[bold green]Removed files:[/bold green]")
            console.print(output)
            print_success("Cleaned untracked files")
        else:
            print_info("No untracked files to remove")
        
        log_command('clean', True, "Removed untracked files")
        
    except Exception as e:
        print_error(f"Failed to clean files: {str(e)}")
        log_command('clean', False, str(e))
