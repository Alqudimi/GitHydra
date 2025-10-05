"""Enhanced diff command"""

import click
from src.ui.console import console, print_error, print_info, print_diff
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.command('diff')
@click.argument('path', required=False)
@click.option('--cached', is_flag=True, help='Show staged changes')
@click.option('--stat', is_flag=True, help='Show statistics only')
@click.option('--commit', help='Compare with specific commit')
def diff_cmd(path, cached, stat, commit):
    """Show changes between commits, commit and working tree, etc"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = []
        
        if stat:
            args.append('--stat')
        
        if cached:
            args.append('--cached')
        
        if commit:
            args.append(commit)
        
        if path:
            args.append('--')
            args.append(path)
        
        diff = repo.git.diff(*args)
        
        if diff:
            if stat:
                console.print(diff)
            else:
                print_diff(diff)
        else:
            print_info("No changes to show")
        
        log_command('diff', True)
        
    except Exception as e:
        print_error(f"Failed to show diff: {str(e)}")
        log_command('diff', False, str(e))
