"""Log and history commands"""

import click
from src.ui.console import console, print_error, create_table
from src.utils.git_helper import get_repo, get_commit_history
from src.logger import log_command

@click.command('log')
@click.option('--max-count', '-n', default=10, help='Limit the number of commits', type=int)
@click.option('--oneline', is_flag=True, help='Show compact format')
@click.option('--graph', is_flag=True, help='Show commit graph')
def log_cmd(max_count, oneline, graph):
    """Show commit history"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        commits = get_commit_history(repo, max_count)
        
        if not commits:
            print_error("No commits yet")
            return
        
        if oneline:
            for commit in commits:
                console.print(f"[yellow]{commit['hash']}[/yellow] {commit['message']}")
        elif graph:
            console.print("[bold cyan]Commit Graph[/bold cyan]")
            for i, commit in enumerate(commits):
                prefix = "* " if i == 0 else "| "
                console.print(f"[yellow]{prefix}{commit['hash']}[/yellow] - {commit['message']}")
                console.print(f"[dim]{' ' * len(prefix)}Author: {commit['author']}, Date: {commit['date']}[/dim]")
        else:
            table = create_table(
                "Commit History",
                ["Hash", "Author", "Date", "Message"]
            )
            
            for commit in commits:
                table.add_row(
                    f"[yellow]{commit['hash']}[/yellow]",
                    commit['author'],
                    commit['date'],
                    commit['message']
                )
            
            console.print(table)
        
        log_command('log', True)
        
    except Exception as e:
        print_error(f"Failed to show log: {str(e)}")
        log_command('log', False, str(e))
