"""Status command"""

import click
from src.ui.console import console, print_info, print_success, create_table, create_panel
from src.utils.git_helper import get_repo, get_modified_files, get_untracked_files, get_staged_files
from src.logger import log_command

@click.command('status')
@click.option('--short', '-s', is_flag=True, help='Show short format')
def status_cmd(short):
    """Show the working tree status"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        try:
            current_branch = repo.active_branch.name
        except:
            current_branch = 'main (no commits yet)'
        
        staged = get_staged_files(repo)
        modified = get_modified_files(repo)
        untracked = get_untracked_files(repo)
        
        if short:
            if staged:
                for f in staged:
                    console.print(f"[green]A  {f}[/green]")
            if modified:
                for f in modified:
                    console.print(f"[red]M  {f}[/red]")
            if untracked:
                for f in untracked:
                    console.print(f"[yellow]?? {f}[/yellow]")
        else:
            panel_content = f"[bold cyan]On branch:[/bold cyan] [bold yellow]{current_branch}[/bold yellow]\n\n"
            
            if staged:
                panel_content += "[bold green]Changes to be committed:[/bold green]\n"
                for f in staged:
                    panel_content += f"  [green]modified: {f}[/green]\n"
                panel_content += "\n"
            
            if modified:
                panel_content += "[bold red]Changes not staged for commit:[/bold red]\n"
                for f in modified:
                    panel_content += f"  [red]modified: {f}[/red]\n"
                panel_content += "\n"
            
            if untracked:
                panel_content += "[bold yellow]Untracked files:[/bold yellow]\n"
                for f in untracked:
                    panel_content += f"  [yellow]{f}[/yellow]\n"
                panel_content += "\n"
            
            if not staged and not modified and not untracked:
                panel_content += "[green]Nothing to commit, working tree clean[/green]"
            
            console.print(create_panel(panel_content, "Repository Status"))
        
        log_command('status', True)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        log_command('status', False, str(e))
