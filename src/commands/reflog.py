"""Reflog management commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_table
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.group('reflog')
def reflog_cmd():
    """Reference log operations"""
    pass

@reflog_cmd.command('show')
@click.argument('ref', default='HEAD')
@click.option('--max-count', '-n', default=20, type=int, help='Limit number of entries')
@click.option('--date', type=click.Choice(['relative', 'iso', 'short']), default='relative', help='Date format')
def show_reflog(ref, max_count, date):
    """Show reflog entries"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.reflog('show', ref, f'-{max_count}', f'--date={date}')
        
        if not output:
            print_info(f"No reflog entries for '{ref}'")
            return
        
        lines = output.strip().split('\n')
        table = create_table(f"Reflog for {ref}", ["Entry", "Commit", "Action", "Message"])
        
        for i, line in enumerate(lines):
            if ':' in line:
                parts = line.split(':', 1)
                ref_part = parts[0].strip()
                message_part = parts[1].strip() if len(parts) > 1 else ''
                
                ref_parts = ref_part.split()
                commit_hash = ref_parts[0][:7] if ref_parts else ''
                entry_num = f"[yellow]@{{{i}}}[/yellow]"
                
                action = ''
                message = message_part
                if ':' in message_part:
                    action_parts = message_part.split(':', 1)
                    action = action_parts[0].strip()
                    message = action_parts[1].strip() if len(action_parts) > 1 else ''
                
                table.add_row(entry_num, f"[cyan]{commit_hash}[/cyan]", action, message[:50])
        
        console.print(table)
        log_command('reflog show', True, f"Showed reflog for {ref}")
        
    except Exception as e:
        print_error(f"Failed to show reflog: {str(e)}")
        log_command('reflog show', False, str(e))

@reflog_cmd.command('expire')
@click.option('--expire', default='90.days.ago', help='Expire entries older than time')
@click.option('--all', is_flag=True, help='Process all reflogs')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be expired')
def expire_reflog(expire, all, dry_run):
    """Expire old reflog entries"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['expire', f'--expire={expire}']
        
        if all:
            args.append('--all')
        
        if dry_run:
            args.append('--dry-run')
            output = repo.git.reflog(*args)
            if output:
                console.print(output)
            else:
                print_info("No reflog entries would be expired")
        else:
            repo.git.reflog(*args)
            print_success(f"Expired reflog entries older than {expire}")
        
        log_command('reflog expire', True, f"Expired entries older than {expire}")
        
    except Exception as e:
        print_error(f"Failed to expire reflog: {str(e)}")
        log_command('reflog expire', False, str(e))

@reflog_cmd.command('delete')
@click.argument('refs', nargs=-1, required=True)
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be deleted')
def delete_reflog(refs, dry_run):
    """Delete specific reflog entries"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['delete']
        if dry_run:
            args.append('--dry-run')
        args.extend(refs)
        
        if dry_run:
            print_info(f"Would delete reflog entries: {', '.join(refs)}")
        else:
            repo.git.reflog(*args)
            print_success(f"Deleted {len(refs)} reflog entry(ies)")
        
        log_command('reflog delete', True, f"Deleted {len(refs)} entries")
        
    except Exception as e:
        print_error(f"Failed to delete reflog entries: {str(e)}")
        log_command('reflog delete', False, str(e))

@reflog_cmd.command('exists')
@click.argument('ref')
def exists_reflog(ref):
    """Check if a reflog exists"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        try:
            repo.git.reflog('exists', ref)
            print_success(f"Reflog exists for '{ref}'")
            log_command('reflog exists', True, f"Reflog exists for {ref}")
        except:
            print_info(f"No reflog found for '{ref}'")
            log_command('reflog exists', True, f"No reflog for {ref}")
        
    except Exception as e:
        print_error(f"Failed to check reflog: {str(e)}")
        log_command('reflog exists', False, str(e))
