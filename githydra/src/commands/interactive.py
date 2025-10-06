"""Interactive menu interface for GitHydra - Enhanced with beautiful UI"""

import click
import questionary
import subprocess
import sys
from pathlib import Path
from githydra.src.ui.console import (
    console, print_success, print_error, create_panel, print_banner,
    print_section_header, ICONS, create_professional_table, print_footer,
    show_loading_animation, print_animated_notification, create_colorful_list
)
from githydra.src.logger import log_command

MAIN_MENU = {
    '1': (f'{ICONS["git"]} Repository Operations', [
        ('1', f'{ICONS["folder"]} Initialize new repository', 'init'),
        ('2', f'{ICONS["download"]} Clone repository', 'sync clone'),
        ('3', f'{ICONS["magnify"]} Show status', 'status'),
        ('4', f'{ICONS["package"]} Create archive', 'archive'),
        ('5', f'{ICONS["trash"]} Clean untracked files', 'clean'),
    ]),
    '2': (f'{ICONS["file"]} File & Staging', [
        ('1', f'{ICONS["plus"]} Stage files (interactive)', 'stage add --interactive'),
        ('2', f'{ICONS["check"]} Stage all files', 'stage add --all'),
        ('3', f'{ICONS["minus"]} Unstage files', 'stage remove --all'),
        ('4', f'{ICONS["magnify"]} Show diff', 'stage diff'),
        ('5', f'{ICONS["book"]} Show file blame', 'blame'),
    ]),
    '3': (f'{ICONS["commit"]} Commits & History', [
        ('1', f'{ICONS["save"]} Create commit', 'commit'),
        ('2', f'{ICONS["wrench"]} Amend last commit', 'commit --amend'),
        ('3', f'{ICONS["book"]} View commit log', 'log'),
        ('4', f'{ICONS["chart"]} View log graph', 'log --graph'),
        ('5', f'{ICONS["clock"]} Show reflog', 'reflog show'),
        ('6', f'{ICONS["file"]} Add note to commit', 'notes add'),
    ]),
    '4': (f'{ICONS["branch"]} Branches', [
        ('1', f'{ICONS["magnify"]} List branches', 'branch list'),
        ('2', f'{ICONS["plus"]} Create branch', 'branch create'),
        ('3', f'{ICONS["arrow"]} Switch branch', 'branch switch'),
        ('4', f'{ICONS["trash"]} Delete branch', 'branch delete'),
        ('5', f'{ICONS["merge"]} Merge branch', 'branch merge'),
        ('6', f'{ICONS["chart"]} Compare branches', 'compare branches'),
    ]),
    '5': (f'{ICONS["remote"]} Remote & Sync', [
        ('1', f'{ICONS["magnify"]} List remotes', 'remote list -v'),
        ('2', f'{ICONS["plus"]} Add remote', 'remote add'),
        ('3', f'{ICONS["upload"]} Push to remote', 'sync push'),
        ('4', f'{ICONS["download"]} Pull from remote', 'sync pull'),
        ('5', f'{ICONS["sync"]} Fetch updates', 'sync fetch'),
        ('6', f'{ICONS["chart"]} Compare with remote', 'compare with-remote'),
    ]),
    '6': (f'{ICONS["sparkles"]} Advanced Operations', [
        ('1', f'{ICONS["save"]} Stash changes', 'stash save'),
        ('2', f'{ICONS["magnify"]} List stashes', 'stash list'),
        ('3', f'{ICONS["arrow"]} Apply stash', 'stash apply'),
        ('4', f'{ICONS["tag"]} Create tag', 'tag create'),
        ('5', f'{ICONS["magnify"]} List tags', 'tag list'),
        ('6', f'{ICONS["wrench"]} Reset changes', 'reset'),
        ('7', f'{ICONS["star"]} Cherry-pick commit', 'cherry-pick'),
        ('8', f'{ICONS["wrench"]} Start rebase', 'rebase start'),
    ]),
    '7': (f'{ICONS["package"]} Submodules & Worktrees', [
        ('1', f'{ICONS["plus"]} Add submodule', 'submodule add'),
        ('2', f'{ICONS["sync"]} Update submodules', 'submodule update'),
        ('3', f'{ICONS["magnify"]} Submodule status', 'submodule status'),
        ('4', f'{ICONS["plus"]} Add worktree', 'worktree add'),
        ('5', f'{ICONS["magnify"]} List worktrees', 'worktree list'),
        ('6', f'{ICONS["trash"]} Remove worktree', 'worktree remove'),
    ]),
    '8': (f'{ICONS["magnify"]} Debugging & Search', [
        ('1', f'{ICONS["rocket"]} Start bisect', 'bisect start'),
        ('2', f'{ICONS["success"]} Mark commit good', 'bisect good'),
        ('3', f'{ICONS["error"]} Mark commit bad', 'bisect bad'),
        ('4', f'{ICONS["check"]} End bisect', 'bisect reset'),
        ('5', f'{ICONS["book"]} File blame', 'blame'),
    ]),
    '9': (f'{ICONS["file"]} Patches & Bundles', [
        ('1', f'{ICONS["save"]} Create patch', 'patch create'),
        ('2', f'{ICONS["arrow"]} Apply patch', 'patch apply'),
        ('3', f'{ICONS["wrench"]} Format patches', 'patch format'),
        ('4', f'{ICONS["package"]} Create bundle', 'bundle create'),
        ('5', f'{ICONS["shield"]} Verify bundle', 'bundle verify'),
    ]),
    'a': (f'{ICONS["warning"]} Conflicts & Merging', [
        ('1', f'{ICONS["magnify"]} List conflicts', 'conflicts list'),
        ('2', f'{ICONS["magnify"]} Show conflicts', 'conflicts show'),
        ('3', f'{ICONS["check"]} Accept ours', 'conflicts ours'),
        ('4', f'{ICONS["check"]} Accept theirs', 'conflicts theirs'),
        ('5', f'{ICONS["cross"]} Abort merge', 'conflicts abort'),
    ]),
    'b': (f'{ICONS["chart"]} Statistics & Analysis', [
        ('1', f'{ICONS["chart"]} Repository overview', 'stats overview'),
        ('2', f'{ICONS["star"]} Contributor stats', 'stats contributors'),
        ('3', f'{ICONS["clock"]} Activity stats', 'stats activity'),
        ('4', f'{ICONS["file"]} File statistics', 'stats files'),
        ('5', f'{ICONS["chart"]} Language analysis', 'stats languages'),
    ]),
    'c': (f'{ICONS["wrench"]} Maintenance & Repair', [
        ('1', f'{ICONS["shield"]} Check repository integrity', 'repair fsck'),
        ('2', f'{ICONS["sparkles"]} Optimize repository', 'repair gc'),
        ('3', f'{ICONS["trash"]} Clean unused objects', 'repair prune'),
        ('4', f'{ICONS["wrench"]} Repair index', 'repair index'),
        ('5', f'{ICONS["info"]} Show repository info', 'repair info'),
    ]),
    'd': (f'{ICONS["wrench"]} Configuration', [
        ('1', f'{ICONS["magnify"]} List configuration', 'config list'),
        ('2', f'{ICONS["wrench"]} Set configuration', 'config set'),
        ('3', f'{ICONS["magnify"]} List aliases', 'alias list'),
        ('4', f'{ICONS["plus"]} Add alias', 'alias add'),
    ]),
    'e': (f'{ICONS["remote"]} Cloud Integration', [
        ('1', f'{ICONS["shield"]} Connect to GitHub', 'cloud connect-github'),
        ('2', f'{ICONS["git"]} List repositories', 'cloud repos'),
        ('3', f'{ICONS["sync"]} Sync with GitHub', 'cloud sync'),
        ('4', f'{ICONS["save"]} Backup repository', 'cloud backup'),
        ('5', f'{ICONS["file"]} List issues', 'cloud issues'),
        ('6', f'{ICONS["tag"]} List releases', 'cloud releases'),
    ]),
    'f': (f'{ICONS["chart"]} Project Management', [
        ('1', f'{ICONS["sparkles"]} Initialize project', 'project init'),
        ('2', f'{ICONS["plus"]} Create issue', 'project issue-create'),
        ('3', f'{ICONS["magnify"]} List issues', 'project issues'),
        ('4', f'{ICONS["star"]} Create milestone', 'project milestone-create'),
        ('5', f'{ICONS["magnify"]} List milestones', 'project milestones'),
        ('6', f'{ICONS["chart"]} Show project board', 'project board'),
    ]),
    'g': (f'{ICONS["star"]} Team Collaboration', [
        ('1', f'{ICONS["star"]} List contributors', 'team contributors'),
        ('2', f'{ICONS["chart"]} Show team activity', 'team activity'),
        ('3', f'{ICONS["merge"]} List pull requests', 'team pr-list'),
        ('4', f'{ICONS["magnify"]} Review branch', 'team review'),
        ('5', f'{ICONS["sparkles"]} Show workflow guide', 'team workflow'),
    ]),
    
'h': (f'{ICONS["sparkles"]} Template Management', [
    ('1', f'{ICONS["magnify"]} List templates', 'template list'),
    ('2', f'{ICONS["plus"]} Add template', 'template add'),
    ('3', f'{ICONS["trash"]} Remove template', 'template remove'),
    ('4', f'{ICONS["rocket"]} Create from template', 'template create'),
    ('5', f'{ICONS["upload"]} Export templates', 'template export'),
    ('6', f'{ICONS["download"]} Import templates', 'template import'),
]),
}

def display_main_menu():
    """Display the beautiful main menu with branding"""
    console.clear()
    
    print_banner()
    
    print_section_header("Main Menu", ICONS['git'])
    
    items = []
    for key, (category, _) in MAIN_MENU.items():
        items.append((f"[bold yellow]{key.upper()}[/bold yellow].", category, "bright_white"))
    
    items.append((f"[bold yellow]0[/bold yellow].", f"{ICONS['cross']} Exit", "bright_white"))
    
    menu_content = create_colorful_list(items, "")
    
    console.print(create_panel(
        menu_content, 
        f"{ICONS['rocket']} Select a Category",
        "bright_cyan",
        "[dim]Choose a number or letter to continue[/dim]"
    ))

def display_category_menu(category_key):
    """Display category submenu with beautiful formatting"""
    console.clear()
    
    category_name, options = MAIN_MENU[category_key]
    
    print_section_header(category_name, ICONS['arrow'])
    
    items = []
    for key, description, _ in options:
        items.append((f"[bold yellow]{key}[/bold yellow].", description, "bright_white"))
    
    items.append((f"[bold yellow]0[/bold yellow].", f"{ICONS['arrow']} Back to main menu", "bright_white"))
    
    menu_content = create_colorful_list(items, "")
    
    console.print(create_panel(
        menu_content, 
        f"{ICONS['sparkles']} Available Commands",
        "bright_magenta",
        "[dim]Enter your choice[/dim]"
    ))

@click.command('interactive')
def interactive_cmd():
    """Launch interactive menu interface with beautiful UI"""
    
    try:
        while True:
            try:
                display_main_menu()
                
                choice = questionary.text(
                    f"{ICONS['arrow']} Enter your choice:",
                    validate=lambda x: x.lower() in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
                ).ask()
                
                if not choice:
                    continue
                
                choice = choice.lower()
                
                if choice == '0':
                    console.clear()
                    print_section_header("Thank You", ICONS['sparkles'])
                    console.print(f"\n{ICONS['success']} [bold green]Thank you for using Githydra![/bold green]\n")
                    print_footer()
                    break
                
                if choice not in MAIN_MENU:
                    print_error("Invalid choice. Please try again.")
                    continue
                
                category_name, options = MAIN_MENU[choice]
                
                while True:
                    try:
                        display_category_menu(choice)
                        
                        sub_choice = questionary.text(
                            f"{ICONS['arrow']} Enter your choice:",
                            validate=lambda x: x in ['0'] + [opt[0] for opt in options]
                        ).ask()
                        
                        if sub_choice == '0':
                            break
                        
                        selected_option = next((opt for opt in options if opt[0] == sub_choice), None)
                        
                        if selected_option:
                            _, description, command = selected_option
                            
                            print_section_header("Executing Command", ICONS['rocket'])
                            console.print(f"\n{ICONS['fire']} [bold cyan]Command:[/bold cyan] [yellow]{description}[/yellow]\n")
                            
                            parts = command.split()
                            
                            githydra_path = Path(__file__).parent.parent.parent / '__main__.py'
                            
                            try:
                                result = subprocess.run(
                                    [sys.executable, str(githydra_path)] + parts,
                                    capture_output=False,
                                    check=False
                                )
                                
                                console.print()
                                
                                if result.returncode != 0:
                                    print_animated_notification(
                                        f"Command failed with exit code {result.returncode}",
                                        "error",
                                        1.0
                                    )
                                    log_command(f"interactive: {command}", False, f"Exit code: {result.returncode}")
                                else:
                                    print_animated_notification(
                                        "Command executed successfully",
                                        "success",
                                        1.0
                                    )
                                    log_command(f"interactive: {command}", True)
                                    
                            except FileNotFoundError as e:
                                print_error(f"Command not found: {str(e)}")
                                log_command(f"interactive: {command}", False, f"FileNotFoundError: {str(e)}")
                            except PermissionError as e:
                                print_error(f"Permission denied: {str(e)}")
                                log_command(f"interactive: {command}", False, f"PermissionError: {str(e)}")
                            except Exception as e:
                                print_error(f"Failed to execute command: {str(e)}")
                                log_command(f"interactive: {command}", False, str(e))
                                console.print_exception(show_locals=False)
                            
                            questionary.text(f"\n{ICONS['arrow']} Press Enter to continue...").ask()
                    
                    except KeyboardInterrupt:
                        console.print(f"\n\n{ICONS['warning']} [yellow]Operation cancelled by user[/yellow]\n")
                        break
                    except Exception as e:
                        print_error(f"Menu error: {str(e)}")
                        console.print_exception(show_locals=False)
                        questionary.text(f"\n{ICONS['arrow']} Press Enter to continue...").ask()
                        break
            
            except KeyboardInterrupt:
                console.print(f"\n\n{ICONS['warning']} [yellow]Returning to main menu...[/yellow]\n")
                continue
            except Exception as e:
                print_error(f"Unexpected error in main menu: {str(e)}")
                console.print_exception(show_locals=False)
                break
    
    except KeyboardInterrupt:
        console.clear()
        console.print(f"\n{ICONS['cross']} [yellow]Githydra interrupted by user[/yellow]\n")
        print_footer()
    except Exception as e:
        print_error(f"Critical error in interactive mode: {str(e)}")
        console.print_exception(show_locals=False)
