"""Conflict resolution helper commands"""

import click
from pathlib import Path
from githydra.src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command
import questionary

@click.group('conflicts')
def conflicts_cmd():
    """Conflict resolution helpers"""
    pass

@conflicts_cmd.command('list')
def list_conflicts():
    """List files with merge conflicts"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        conflicted_files = []
        unmerged = repo.index.unmerged_blobs()
        
        if not unmerged:
            print_success("No conflicts found!")
            return
        
        for file_path in unmerged.keys():
            conflicted_files.append(file_path)
        
        table = create_table("Conflicted Files", ["File", "Status"])
        
        for file in conflicted_files:
            table.add_row(f"[red]{file}[/red]", "[yellow]Unmerged[/yellow]")
        
        console.print(table)
        
        panel_content = "[bold cyan]Resolution Steps:[/bold cyan]\n\n"
        panel_content += "1. Edit files to resolve conflicts\n"
        panel_content += "2. Use '[yellow]githydra conflicts resolve <file>[/yellow]' to mark as resolved\n"
        panel_content += "3. Use '[yellow]githydra conflicts ours/theirs <file>[/yellow]' to choose a version\n"
        panel_content += "4. Use '[yellow]githydra commit[/yellow]' to complete the merge"
        
        console.print(create_panel(panel_content, "How to Resolve"))
        
        log_command('conflicts list', True, f"Found {len(conflicted_files)} conflicts")
        
    except Exception as e:
        print_error(f"Failed to list conflicts: {str(e)}")
        log_command('conflicts list', False, str(e))

@conflicts_cmd.command('show')
@click.argument('file')
def show_conflict(file):
    """Show conflict markers in a file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        file_path = Path(repo.working_dir) / file
        
        if not file_path.exists():
            print_error(f"File not found: {file}")
            return
        
        content = file_path.read_text()
        
        if '<<<<<<<' not in content:
            print_info(f"No conflict markers found in {file}")
            return
        
        console.print(f"[bold cyan]Conflicts in {file}:[/bold cyan]\n")
        
        in_conflict = False
        for line in content.split('\n'):
            if line.startswith('<<<<<<<'):
                console.print(f"[red]{line}[/red]")
                in_conflict = True
            elif line.startswith('======='):
                console.print(f"[yellow]{line}[/yellow]")
            elif line.startswith('>>>>>>>'):
                console.print(f"[red]{line}[/red]")
                in_conflict = False
            elif in_conflict:
                console.print(f"[dim]{line}[/dim]")
            else:
                console.print(line)
        
        log_command('conflicts show', True, f"Showed conflicts in {file}")
        
    except Exception as e:
        print_error(f"Failed to show conflicts: {str(e)}")
        log_command('conflicts show', False, str(e))

@conflicts_cmd.command('ours')
@click.argument('files', nargs=-1, required=True)
def accept_ours(files):
    """Accept 'our' version for conflicted files"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        for file in files:
            repo.git.checkout('--ours', file)
            repo.index.add([file])
        
        print_success(f"Accepted 'ours' version for {len(files)} file(s)")
        log_command('conflicts ours', True, f"Accepted ours for {len(files)} files")
        
    except Exception as e:
        print_error(f"Failed to accept 'ours': {str(e)}")
        log_command('conflicts ours', False, str(e))

@conflicts_cmd.command('theirs')
@click.argument('files', nargs=-1, required=True)
def accept_theirs(files):
    """Accept 'their' version for conflicted files"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        for file in files:
            repo.git.checkout('--theirs', file)
            repo.index.add([file])
        
        print_success(f"Accepted 'theirs' version for {len(files)} file(s)")
        log_command('conflicts theirs', True, f"Accepted theirs for {len(files)} files")
        
    except Exception as e:
        print_error(f"Failed to accept 'theirs': {str(e)}")
        log_command('conflicts theirs', False, str(e))

@conflicts_cmd.command('resolve')
@click.argument('files', nargs=-1)
@click.option('--all', '-a', is_flag=True, help='Mark all conflicted files as resolved')
def mark_resolved(files, all):
    """Mark files as resolved and stage them"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if all:
            unmerged = repo.index.unmerged_blobs()
            files = list(unmerged.keys())
        
        if not files:
            print_error("No files specified")
            return
        
        for file in files:
            repo.index.add([file])
        
        print_success(f"Marked {len(files)} file(s) as resolved")
        log_command('conflicts resolve', True, f"Resolved {len(files)} files")
        
    except Exception as e:
        print_error(f"Failed to mark as resolved: {str(e)}")
        log_command('conflicts resolve', False, str(e))

@conflicts_cmd.command('abort')
def abort_merge():
    """Abort the current merge and return to pre-merge state"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        confirm = questionary.confirm(
            "Are you sure you want to abort the merge? All conflict resolutions will be lost.",
            default=False
        ).ask()
        
        if not confirm:
            print_info("Abort cancelled")
            return
        
        repo.git.merge('--abort')
        print_success("Merge aborted successfully")
        log_command('conflicts abort', True)
        
    except Exception as e:
        print_error(f"Failed to abort merge: {str(e)}")
        log_command('conflicts abort', False, str(e))

@conflicts_cmd.command('tool')
@click.argument('file', required=False)
@click.option('--tool', '-t', help='Merge tool to use')
def launch_merge_tool(file, tool):
    """Launch external merge tool"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['mergetool']
        
        if tool:
            args.extend(['--tool', tool])
        
        if file:
            args.append(file)
        
        repo.git.execute(args)
        print_success("Merge tool completed")
        log_command('conflicts tool', True)
        
    except Exception as e:
        print_error(f"Failed to launch merge tool: {str(e)}")
        log_command('conflicts tool', False, str(e))
