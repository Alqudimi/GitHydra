"""Repository repair and maintenance commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_panel, create_progress
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.group('repair')
def repair_cmd():
    """Repository maintenance and repair operations"""
    pass

@repair_cmd.command('fsck')
@click.option('--full', is_flag=True, help='Full integrity check')
def fsck(full):
    """Check repository integrity"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        print_info("Checking repository integrity...")
        
        with create_progress() as progress:
            task = progress.add_task("Running fsck...", total=100)
            
            if full:
                result = repo.git.fsck('--full')
            else:
                result = repo.git.fsck()
            
            progress.update(task, completed=100)
        
        if result:
            console.print(f"[dim]{result}[/dim]")
        
        print_success("Repository integrity check completed successfully")
        log_command('repair fsck', True)
        
    except Exception as e:
        print_error(f"Integrity check failed: {str(e)}")
        log_command('repair fsck', False, str(e))

@repair_cmd.command('gc')
@click.option('--aggressive', is_flag=True, help='Aggressive optimization')
def gc(aggressive):
    """Optimize and clean up repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        print_info("Optimizing repository...")
        
        with create_progress() as progress:
            task = progress.add_task("Running garbage collection...", total=100)
            
            if aggressive:
                result = repo.git.gc('--aggressive', '--prune=now')
            else:
                result = repo.git.gc('--auto')
            
            progress.update(task, completed=100)
        
        print_success("Repository optimized successfully")
        log_command('repair gc', True)
        
    except Exception as e:
        print_error(f"Optimization failed: {str(e)}")
        log_command('repair gc', False, str(e))

@repair_cmd.command('prune')
@click.option('--dry-run', is_flag=True, help='Show what would be deleted')
def prune(dry_run):
    """Remove unreachable objects"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if dry_run:
            print_info("Showing objects that would be pruned...")
            result = repo.git.prune('--dry-run', '-v')
        else:
            print_info("Pruning unreachable objects...")
            result = repo.git.prune('-v')
        
        if result:
            console.print(f"[dim]{result}[/dim]")
        
        print_success("Prune completed successfully")
        log_command('repair prune', True)
        
    except Exception as e:
        print_error(f"Prune failed: {str(e)}")
        log_command('repair prune', False, str(e))

@repair_cmd.command('index')
def repair_index():
    """Repair corrupted index"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        print_info("Repairing repository index...")
        
        repo.git.read_tree('HEAD')
        
        print_success("Index repaired successfully")
        log_command('repair index', True)
        
    except Exception as e:
        print_error(f"Index repair failed: {str(e)}")
        log_command('repair index', False, str(e))

@repair_cmd.command('info')
def repo_info():
    """Display repository information and statistics"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        info_content = ""
        
        try:
            branch = repo.active_branch.name
            info_content += f"[bold cyan]Current Branch:[/bold cyan] {branch}\n"
        except:
            info_content += f"[bold cyan]Current Branch:[/bold cyan] (detached HEAD)\n"
        
        try:
            commit_count = len(list(repo.iter_commits()))
            info_content += f"[bold cyan]Total Commits:[/bold cyan] {commit_count}\n"
        except:
            info_content += f"[bold cyan]Total Commits:[/bold cyan] 0\n"
        
        branch_count = len(list(repo.branches))
        info_content += f"[bold cyan]Total Branches:[/bold cyan] {branch_count}\n"
        
        remote_count = len(list(repo.remotes))
        info_content += f"[bold cyan]Total Remotes:[/bold cyan] {remote_count}\n"
        
        try:
            size_info = repo.git.count_objects('-v', '-H')
            info_content += f"\n[bold cyan]Storage Information:[/bold cyan]\n[dim]{size_info}[/dim]"
        except:
            pass
        
        console.print(create_panel(info_content, "Repository Information"))
        log_command('repair info', True)
        
    except Exception as e:
        print_error(f"Failed to get repository info: {str(e)}")
        log_command('repair info', False, str(e))
