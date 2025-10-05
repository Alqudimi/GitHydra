"""Initialize repository command"""

import click
import git
from pathlib import Path
from src.ui.console import console, print_success, print_error, create_panel
from src.logger import log_command

@click.command('init')
@click.argument('path', default='.', type=click.Path())
@click.option('--bare', is_flag=True, help='Create a bare repository')
def init_cmd(path, bare):
    """Initialize a new Git repository"""
    try:
        repo_path = Path(path).resolve()
        
        if bare:
            repo = git.Repo.init(repo_path, bare=True)
            print_success(f"Initialized empty bare Git repository in {repo_path}")
        else:
            repo = git.Repo.init(repo_path)
            print_success(f"Initialized empty Git repository in {repo_path}")
        
        panel_content = f"[bold cyan]Repository Location:[/bold cyan] {repo_path}\n"
        panel_content += f"[bold cyan]Repository Type:[/bold cyan] {'Bare' if bare else 'Standard'}\n"
        
        try:
            branch_name = repo.active_branch.name if not bare else 'main'
        except:
            branch_name = 'main'
        
        panel_content += f"[bold cyan]Default Branch:[/bold cyan] {branch_name}"
        
        console.print(create_panel(panel_content, "Repository Information"))
        log_command('init', True, f"Repository initialized at {repo_path}")
        
    except Exception as e:
        print_error(f"Failed to initialize repository: {str(e)}")
        log_command('init', False, str(e))
