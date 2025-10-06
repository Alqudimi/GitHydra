"""Git notes commands for adding annotations to commits"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command
import questionary

@click.group('notes')
def notes_cmd():
    """Add and manage commit notes"""
    pass

@notes_cmd.command('add')
@click.argument('commit', default='HEAD')
@click.option('--message', '-m', help='Note message')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing note')
@click.option('--ref', default='commits', help='Notes ref to use')
def add_note(commit, message, force, ref):
    """Add a note to a commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not message:
            message = questionary.text(
                "Enter note message:",
                multiline=True
            ).ask()
            
            if not message:
                print_error("Note cancelled: no message provided")
                return
        
        args = ['add']
        if force:
            args.append('-f')
        args.extend(['-m', message, '--ref', ref, commit])
        
        repo.git.notes(*args)
        print_success(f"Added note to commit {commit}")
        
        panel_content = f"[bold cyan]Commit:[/bold cyan] {commit}\n"
        panel_content += f"[bold cyan]Note:[/bold cyan] {message}"
        
        console.print(create_panel(panel_content, "Note Added"))
        log_command('notes add', True, f"Added note to {commit}")
        
    except Exception as e:
        print_error(f"Failed to add note: {str(e)}")
        log_command('notes add', False, str(e))

@notes_cmd.command('show')
@click.argument('commit', default='HEAD')
@click.option('--ref', default='commits', help='Notes ref to use')
def show_note(commit, ref):
    """Show note for a commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.notes('show', '--ref', ref, commit)
        
        if not output:
            print_info(f"No note found for commit {commit}")
            return
        
        console.print(create_panel(output, f"Note for {commit}"))
        log_command('notes show', True)
        
    except Exception as e:
        if 'no note found' in str(e).lower():
            print_info(f"No note found for commit {commit}")
        else:
            print_error(f"Failed to show note: {str(e)}")
        log_command('notes show', False, str(e))

@notes_cmd.command('list')
@click.argument('commit', required=False)
@click.option('--ref', default='commits', help='Notes ref to use')
def list_notes(commit, ref):
    """List notes"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['list', '--ref', ref]
        if commit:
            args.append(commit)
        
        output = repo.git.notes(*args)
        
        if not output:
            print_info("No notes found")
            return
        
        console.print("[bold cyan]Notes:[/bold cyan]")
        console.print(output)
        log_command('notes list', True)
        
    except Exception as e:
        print_error(f"Failed to list notes: {str(e)}")
        log_command('notes list', False, str(e))

@notes_cmd.command('remove')
@click.argument('commit', default='HEAD')
@click.option('--ref', default='commits', help='Notes ref to use')
def remove_note(commit, ref):
    """Remove note from a commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.git.notes('remove', '--ref', ref, commit)
        print_success(f"Removed note from commit {commit}")
        log_command('notes remove', True, f"Removed note from {commit}")
        
    except Exception as e:
        print_error(f"Failed to remove note: {str(e)}")
        log_command('notes remove', False, str(e))

@notes_cmd.command('edit')
@click.argument('commit', default='HEAD')
@click.option('--ref', default='commits', help='Notes ref to use')
def edit_note(commit, ref):
    """Edit note for a commit"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        try:
            current_note = repo.git.notes('show', '--ref', ref, commit)
            console.print(f"[cyan]Current note:[/cyan]\n{current_note}\n")
        except:
            current_note = ""
        
        new_message = questionary.text(
            "Enter new note message:",
            multiline=True,
            default=current_note
        ).ask()
        
        if not new_message:
            print_error("Edit cancelled: no message provided")
            return
        
        repo.git.notes('add', '-f', '-m', new_message, '--ref', ref, commit)
        print_success(f"Edited note for commit {commit}")
        log_command('notes edit', True, f"Edited note for {commit}")
        
    except Exception as e:
        print_error(f"Failed to edit note: {str(e)}")
        log_command('notes edit', False, str(e))

@notes_cmd.command('copy')
@click.argument('from_commit')
@click.argument('to_commit')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing note')
@click.option('--ref', default='commits', help='Notes ref to use')
def copy_note(from_commit, to_commit, force, ref):
    """Copy note from one commit to another"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['copy']
        if force:
            args.append('-f')
        args.extend(['--ref', ref, from_commit, to_commit])
        
        repo.git.notes(*args)
        print_success(f"Copied note from {from_commit} to {to_commit}")
        log_command('notes copy', True, f"Copied note from {from_commit} to {to_commit}")
        
    except Exception as e:
        print_error(f"Failed to copy note: {str(e)}")
        log_command('notes copy', False, str(e))
