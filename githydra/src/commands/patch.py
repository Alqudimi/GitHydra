"""Patch management commands"""

import click
from pathlib import Path
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.group('patch')
def patch_cmd():
    """Patch creation and application"""
    pass

@patch_cmd.command('create')
@click.argument('output')
@click.option('--staged', is_flag=True, help='Create patch from staged changes')
@click.option('--commit', '-c', help='Create patch from specific commit')
def create_patch(output, staged, commit):
    """Create a patch file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output_path = Path(output)
        
        if not output_path.suffix:
            output_path = output_path.with_suffix('.patch')
        
        if staged:
            diff_output = repo.git.diff('--cached')
        elif commit:
            diff_output = repo.git.show(commit)
        else:
            diff_output = repo.git.diff()
        
        if not diff_output:
            print_error("No changes to create patch from")
            return
        
        output_path.write_text(diff_output)
        
        lines = len(diff_output.split('\n'))
        size = output_path.stat().st_size
        
        print_success(f"Created patch: {output_path}")
        
        panel_content = f"[bold cyan]File:[/bold cyan] {output_path}\n"
        panel_content += f"[bold cyan]Lines:[/bold cyan] {lines}\n"
        panel_content += f"[bold cyan]Size:[/bold cyan] {size} bytes"
        
        console.print(create_panel(panel_content, "Patch Created"))
        log_command('patch create', True, f"Created patch: {output_path}")
        
    except Exception as e:
        print_error(f"Failed to create patch: {str(e)}")
        log_command('patch create', False, str(e))

@patch_cmd.command('apply')
@click.argument('patch_file')
@click.option('--check', is_flag=True, help='Check if patch can be applied')
@click.option('--reverse', is_flag=True, help='Apply patch in reverse')
@click.option('--index', is_flag=True, help='Apply to index')
def apply_patch(patch_file, check, reverse, index):
    """Apply a patch file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        patch_path = Path(patch_file)
        
        if not patch_path.exists():
            print_error(f"Patch file not found: {patch_file}")
            return
        
        args = ['apply']
        
        if check:
            args.append('--check')
        
        if reverse:
            args.append('--reverse')
        
        if index:
            args.append('--index')
        
        args.append(str(patch_path))
        
        repo.git.execute(args)
        
        if check:
            print_success("Patch can be applied cleanly")
        else:
            print_success(f"Applied patch: {patch_file}")
        
        log_command('patch apply', True, f"Applied patch: {patch_file}")
        
    except Exception as e:
        print_error(f"Failed to apply patch: {str(e)}")
        log_command('patch apply', False, str(e))

@patch_cmd.command('format')
@click.argument('commit_range')
@click.option('--output-directory', '-o', default='.', help='Output directory for patches')
@click.option('--numbered', '-n', is_flag=True, help='Name files with number prefix')
@click.option('--cover-letter', is_flag=True, help='Generate cover letter')
def format_patch(commit_range, output_directory, numbered, cover_letter):
    """Generate patch files for email submission"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        args = ['format-patch', '-o', str(output_dir)]
        
        if numbered:
            args.append('-n')
        
        if cover_letter:
            args.append('--cover-letter')
        
        args.append(commit_range)
        
        output = repo.git.execute(args)
        
        files = output.strip().split('\n') if output else []
        
        print_success(f"Generated {len(files)} patch file(s)")
        
        panel_content = f"[bold cyan]Output Directory:[/bold cyan] {output_dir}\n"
        panel_content += f"[bold cyan]Files Created:[/bold cyan] {len(files)}\n\n"
        
        for file in files[:10]:
            panel_content += f"  • {Path(file).name}\n"
        
        if len(files) > 10:
            panel_content += f"  ... and {len(files) - 10} more\n"
        
        console.print(create_panel(panel_content, "Patches Generated"))
        log_command('patch format', True, f"Generated {len(files)} patches")
        
    except Exception as e:
        print_error(f"Failed to format patches: {str(e)}")
        log_command('patch format', False, str(e))

@patch_cmd.command('stats')
@click.argument('patch_file')
def patch_stats(patch_file):
    """Show statistics for a patch file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        patch_path = Path(patch_file)
        
        if not patch_path.exists():
            print_error(f"Patch file not found: {patch_file}")
            return
        
        output = repo.git.apply('--stat', str(patch_path))
        
        console.print(create_panel(output, f"Patch Statistics: {patch_file}"))
        log_command('patch stats', True)
        
    except Exception as e:
        print_error(f"Failed to show patch stats: {str(e)}")
        log_command('patch stats', False, str(e))
