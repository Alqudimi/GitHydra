"""Archive creation commands"""

import click
from pathlib import Path
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.command('archive')
@click.argument('output')
@click.option('--ref', default='HEAD', help='Reference to archive (branch, tag, commit)')
@click.option('--format', '-f', type=click.Choice(['zip', 'tar', 'tar.gz', 'tgz']), default='zip', help='Archive format')
@click.option('--prefix', help='Prefix for paths in archive')
@click.option('--remote', help='Archive from remote repository')
def archive_cmd(output, ref, format, prefix, remote):
    """Create an archive of files from a named tree"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output_path = Path(output)
        
        if format == 'tar.gz' or format == 'tgz':
            actual_format = 'tar.gz'
        else:
            actual_format = format
        
        if not output_path.suffix:
            if actual_format == 'tar.gz':
                output_path = output_path.with_suffix('.tar.gz')
            else:
                output_path = output_path.with_suffix(f'.{actual_format}')
        
        args = [f'--format={actual_format}']
        
        if prefix:
            args.append(f'--prefix={prefix}/')
        
        args.append(f'--output={output_path}')
        
        if remote:
            args.extend(['--remote', remote])
        
        args.append(ref)
        
        repo.git.archive(*args)
        
        file_size = output_path.stat().st_size if output_path.exists() else 0
        size_mb = file_size / (1024 * 1024)
        
        print_success(f"Created archive: {output_path}")
        
        panel_content = f"[bold cyan]File:[/bold cyan] {output_path}\n"
        panel_content += f"[bold cyan]Format:[/bold cyan] {actual_format}\n"
        panel_content += f"[bold cyan]Reference:[/bold cyan] {ref}\n"
        panel_content += f"[bold cyan]Size:[/bold cyan] {size_mb:.2f} MB"
        
        console.print(create_panel(panel_content, "Archive Created"))
        log_command('archive', True, f"Created archive: {output_path}")
        
    except Exception as e:
        print_error(f"Failed to create archive: {str(e)}")
        log_command('archive', False, str(e))
