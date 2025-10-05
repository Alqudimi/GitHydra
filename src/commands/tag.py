"""Tag management commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from src.utils.git_helper import get_repo
from src.logger import log_command
import questionary

@click.group('tag')
def tag_cmd():
    """Tag management"""
    pass

@tag_cmd.command('list')
@click.option('--verbose', '-v', is_flag=True, help='Show tag details')
def list_tags(verbose):
    """List all tags"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        tags = repo.tags
        
        if not tags:
            print_info("No tags found")
            return
        
        if verbose:
            table = create_table("Tags", ["Name", "Commit", "Message"])
            
            for tag in tags:
                try:
                    commit_hash = tag.commit.hexsha[:7]
                    message = tag.commit.message.strip().split('\n')[0]
                    table.add_row(tag.name, commit_hash, message)
                except:
                    table.add_row(tag.name, "N/A", "N/A")
            
            console.print(table)
        else:
            for tag in tags:
                console.print(f"[yellow]{tag.name}[/yellow]")
        
        log_command('tag list', True)
        
    except Exception as e:
        print_error(f"Failed to list tags: {str(e)}")
        log_command('tag list', False, str(e))

@tag_cmd.command('create')
@click.argument('tag_name')
@click.option('--message', '-m', help='Tag message')
@click.option('--annotated', '-a', is_flag=True, help='Create annotated tag')
def create_tag(tag_name, message, annotated):
    """Create a new tag"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if annotated or message:
            if not message:
                message = questionary.text("Enter tag message:").ask()
            
            repo.create_tag(tag_name, message=message)
            print_success(f"Created annotated tag '{tag_name}'")
        else:
            repo.create_tag(tag_name)
            print_success(f"Created lightweight tag '{tag_name}'")
        
        log_command('tag create', True, f"Tag '{tag_name}' created")
        
    except Exception as e:
        print_error(f"Failed to create tag: {str(e)}")
        log_command('tag create', False, str(e))

@tag_cmd.command('delete')
@click.argument('tag_name')
def delete_tag(tag_name):
    """Delete a tag"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        repo.delete_tag(tag_name)
        print_success(f"Deleted tag '{tag_name}'")
        log_command('tag delete', True, f"Tag '{tag_name}' deleted")
        
    except Exception as e:
        print_error(f"Failed to delete tag: {str(e)}")
        log_command('tag delete', False, str(e))

@tag_cmd.command('show')
@click.argument('tag_name')
def show_tag(tag_name):
    """Show tag details"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        tag = repo.tags[tag_name]
        
        content = f"[bold cyan]Tag Name:[/bold cyan] {tag.name}\n"
        content += f"[bold cyan]Commit:[/bold cyan] {tag.commit.hexsha[:7]}\n"
        content += f"[bold cyan]Author:[/bold cyan] {tag.commit.author.name}\n"
        content += f"[bold cyan]Date:[/bold cyan] {tag.commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"[bold cyan]Message:[/bold cyan]\n{tag.commit.message.strip()}"
        
        console.print(create_panel(content, f"Tag: {tag_name}"))
        log_command('tag show', True)
        
    except Exception as e:
        print_error(f"Failed to show tag: {str(e)}")
        log_command('tag show', False, str(e))
