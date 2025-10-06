"""Commit commands"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo, get_staged_files
from githydra.src.logger import log_command
import questionary

@click.command('commit')
@click.option('--message', '-m', help='Commit message')
@click.option('--amend', is_flag=True, help='Amend the previous commit')
@click.option('--all', '-a', is_flag=True, help='Stage all modified files and commit')
def commit_cmd(message, amend, all):
    """Create a new commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if all:
            repo.git.add(A=True)
            print_info("Staged all modified files")
        
        staged = get_staged_files(repo)
        
        if not staged and not amend:
            print_error("No changes staged for commit. Use 'githydra stage add' first.")
            return
        
        if not message:
            message = questionary.text(
                "Enter commit message:",
                validate=lambda text: len(text) > 0 or "Message cannot be empty"
            ).ask()
            
            if not message:
                print_error("Commit aborted: no message provided")
                return
        
        if amend:
            repo.git.commit(amend=True, m=message)
            print_success("Amended the previous commit")
        else:
            repo.index.commit(message)
            print_success(f"Created commit: {message}")
        
        try:
            last_commit = repo.head.commit
            panel_content = f"[bold cyan]Commit Hash:[/bold cyan] {last_commit.hexsha[:7]}\n"
            panel_content += f"[bold cyan]Author:[/bold cyan] {last_commit.author.name}\n"
            panel_content += f"[bold cyan]Message:[/bold cyan] {last_commit.message.strip()}"
            
            console.print(create_panel(panel_content, "Commit Information"))
        except:
            pass
        log_command('commit', True, f"Commit created: {message}")
        
    except Exception as e:
        print_error(f"Failed to create commit: {str(e)}")
        log_command('commit', False, str(e))
