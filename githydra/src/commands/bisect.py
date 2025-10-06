"""Git bisect commands for binary search debugging"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.group('bisect')
def bisect_cmd():
    """Binary search to find the commit that introduced a bug"""
    pass

@bisect_cmd.command('start')
@click.argument('bad', required=False)
@click.argument('good', required=False)
def start_bisect(bad, good):
    """Start bisect session"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.bisect('start')
        print_success("Started bisect session")
        
        if bad:
            repo.git.bisect('bad', bad)
            print_info(f"Marked {bad} as bad")
        
        if good:
            repo.git.bisect('good', good)
            print_info(f"Marked {good} as good")
        
        panel_content = "[bold cyan]Bisect Session Started[/bold cyan]\n\n"
        panel_content += "Use '[yellow]githydra bisect good[/yellow]' to mark current commit as good\n"
        panel_content += "Use '[yellow]githydra bisect bad[/yellow]' to mark current commit as bad\n"
        panel_content += "Use '[yellow]githydra bisect reset[/yellow]' to end the session"
        
        console.print(create_panel(panel_content, "Bisect Guide"))
        log_command('bisect start', True)
        
    except Exception as e:
        print_error(f"Failed to start bisect: {str(e)}")
        log_command('bisect start', False, str(e))

@bisect_cmd.command('good')
@click.argument('commits', nargs=-1)
def mark_good(commits):
    """Mark commits as good"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if commits:
            repo.git.bisect('good', *commits)
        else:
            output = repo.git.bisect('good')
            console.print(output)
        
        print_success("Marked commit(s) as good")
        log_command('bisect good', True)
        
    except Exception as e:
        print_error(f"Failed to mark as good: {str(e)}")
        log_command('bisect good', False, str(e))

@bisect_cmd.command('bad')
@click.argument('commits', nargs=-1)
def mark_bad(commits):
    """Mark commits as bad"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if commits:
            repo.git.bisect('bad', *commits)
        else:
            output = repo.git.bisect('bad')
            console.print(output)
        
        print_success("Marked commit(s) as bad")
        log_command('bisect bad', True)
        
    except Exception as e:
        print_error(f"Failed to mark as bad: {str(e)}")
        log_command('bisect bad', False, str(e))

@bisect_cmd.command('skip')
@click.argument('commits', nargs=-1)
def skip_bisect(commits):
    """Skip commits that cannot be tested"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if commits:
            repo.git.bisect('skip', *commits)
        else:
            repo.git.bisect('skip')
        
        print_success("Skipped commit(s)")
        log_command('bisect skip', True)
        
    except Exception as e:
        print_error(f"Failed to skip: {str(e)}")
        log_command('bisect skip', False, str(e))

@bisect_cmd.command('reset')
@click.argument('commit', required=False)
def reset_bisect(commit):
    """End bisect session and return to original HEAD"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if commit:
            repo.git.bisect('reset', commit)
        else:
            repo.git.bisect('reset')
        
        print_success("Bisect session ended")
        log_command('bisect reset', True)
        
    except Exception as e:
        print_error(f"Failed to reset bisect: {str(e)}")
        log_command('bisect reset', False, str(e))

@bisect_cmd.command('log')
def log_bisect():
    """Show bisect log"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.bisect('log')
        
        if not output:
            print_info("No bisect log available")
            return
        
        console.print(create_panel(output, "Bisect Log"))
        log_command('bisect log', True)
        
    except Exception as e:
        print_error(f"Failed to show bisect log: {str(e)}")
        log_command('bisect log', False, str(e))

@bisect_cmd.command('visualize')
@click.option('--gitk', is_flag=True, help='Use gitk for visualization')
def visualize_bisect(gitk):
    """Visualize bisect progress"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if gitk:
            repo.git.bisect('visualize', '--gitk')
        else:
            output = repo.git.bisect('view')
            console.print(output)
        
        log_command('bisect visualize', True)
        
    except Exception as e:
        print_error(f"Failed to visualize bisect: {str(e)}")
        log_command('bisect visualize', False, str(e))
