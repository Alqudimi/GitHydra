"""Interactive menu interface for GitHydra"""

import click
import questionary
import subprocess
import sys
from pathlib import Path
from src.ui.console import console, print_success, print_error, create_panel
from src.logger import log_command

MAIN_MENU = {
    '1': ('Repository Operations', [
        ('1', 'Initialize new repository', 'init'),
        ('2', 'Clone repository', 'sync clone'),
        ('3', 'Show status', 'status'),
    ]),
    '2': ('File & Staging', [
        ('1', 'Stage files (interactive)', 'stage add --interactive'),
        ('2', 'Stage all files', 'stage add --all'),
        ('3', 'Unstage files', 'stage remove --all'),
        ('4', 'Show diff', 'stage diff'),
    ]),
    '3': ('Commits', [
        ('1', 'Create commit', 'commit'),
        ('2', 'Amend last commit', 'commit --amend'),
        ('3', 'View commit log', 'log'),
        ('4', 'View log graph', 'log --graph'),
    ]),
    '4': ('Branches', [
        ('1', 'List branches', 'branch list'),
        ('2', 'Create branch', 'branch create'),
        ('3', 'Switch branch', 'branch switch'),
        ('4', 'Delete branch', 'branch delete'),
        ('5', 'Merge branch', 'branch merge'),
    ]),
    '5': ('Remote & Sync', [
        ('1', 'List remotes', 'remote list -v'),
        ('2', 'Add remote', 'remote add'),
        ('3', 'Push to remote', 'sync push'),
        ('4', 'Pull from remote', 'sync pull'),
        ('5', 'Fetch updates', 'sync fetch'),
    ]),
    '6': ('Advanced Operations', [
        ('1', 'Stash changes', 'stash save'),
        ('2', 'List stashes', 'stash list'),
        ('3', 'Apply stash', 'stash apply'),
        ('4', 'Create tag', 'tag create'),
        ('5', 'List tags', 'tag list'),
        ('6', 'Reset changes', 'reset'),
        ('7', 'Cherry-pick commit', 'cherry-pick'),
    ]),
    '7': ('Maintenance & Repair', [
        ('1', 'Check repository integrity', 'repair fsck'),
        ('2', 'Optimize repository', 'repair gc'),
        ('3', 'Clean unused objects', 'repair prune'),
        ('4', 'Repair index', 'repair index'),
        ('5', 'Show repository info', 'repair info'),
    ]),
    '8': ('Configuration', [
        ('1', 'List configuration', 'config list'),
        ('2', 'Set configuration', 'config set'),
        ('3', 'List aliases', 'alias list'),
        ('4', 'Add alias', 'alias add'),
    ]),
}

def display_main_menu():
    """Display the main menu"""
    console.clear()
    
    title = "[bold cyan]GitHydra - Interactive Git Manager[/bold cyan]"
    menu_content = "\n"
    
    for key, (category, _) in MAIN_MENU.items():
        menu_content += f"[yellow]{key}[/yellow]. {category}\n"
    
    menu_content += "[yellow]0[/yellow]. Exit\n"
    
    console.print(create_panel(menu_content, title))

def display_category_menu(category_key):
    """Display category submenu"""
    console.clear()
    
    category_name, options = MAIN_MENU[category_key]
    title = f"[bold cyan]{category_name}[/bold cyan]"
    menu_content = "\n"
    
    for key, description, _ in options:
        menu_content += f"[yellow]{key}[/yellow]. {description}\n"
    
    menu_content += "[yellow]0[/yellow]. Back to main menu\n"
    
    console.print(create_panel(menu_content, title))

@click.command('interactive')
def interactive_cmd():
    """Launch interactive menu interface"""
    
    while True:
        display_main_menu()
        
        choice = questionary.text(
            "Enter your choice:",
            validate=lambda x: x in [str(i) for i in range(9)]
        ).ask()
        
        if choice == '0':
            print_success("Goodbye!")
            break
        
        if choice not in MAIN_MENU:
            continue
        
        category_name, options = MAIN_MENU[choice]
        
        while True:
            display_category_menu(choice)
            
            sub_choice = questionary.text(
                "Enter your choice:",
                validate=lambda x: x in ['0'] + [opt[0] for opt in options]
            ).ask()
            
            if sub_choice == '0':
                break
            
            selected_option = next((opt for opt in options if opt[0] == sub_choice), None)
            
            if selected_option:
                _, description, command = selected_option
                console.print(f"\n[bold green]Executing:[/bold green] {description}\n")
                
                parts = command.split()
                
                githydra_path = Path(__file__).parent.parent.parent / 'githydra.py'
                
                try:
                    result = subprocess.run(
                        [sys.executable, str(githydra_path)] + parts,
                        capture_output=False,
                        check=False
                    )
                    
                    if result.returncode != 0:
                        print_error(f"\nCommand failed with exit code {result.returncode}")
                        log_command(f"interactive: {command}", False, f"Exit code: {result.returncode}")
                    else:
                        log_command(f"interactive: {command}", True)
                        
                except Exception as e:
                    print_error(f"\nFailed to execute command: {str(e)}")
                    log_command(f"interactive: {command}", False, str(e))
                
                questionary.text("\nPress Enter to continue...").ask()
