"""Git bundle operations for repository transport"""

import click
from pathlib import Path
from githydra.src.ui.console import console, print_success, print_error, print_info, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.group('bundle')
def bundle_cmd():
    """Bundle operations for repository transport"""
    pass

@bundle_cmd.command('create')
@click.argument('file')
@click.argument('refs', nargs=-1)
@click.option('--all', is_flag=True, help='Bundle all refs')
@click.option('--branches', is_flag=True, help='Bundle all branches')
@click.option('--tags', is_flag=True, help='Bundle all tags')
def create_bundle(file, refs, all, branches, tags):
    """Create a bundle file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        bundle_path = Path(file)
        
        if not bundle_path.suffix:
            bundle_path = bundle_path.with_suffix('.bundle')
        
        args = ['bundle', 'create', str(bundle_path)]
        
        if all:
            args.append('--all')
        elif branches:
            args.append('--branches')
        elif tags:
            args.append('--tags')
        elif refs:
            args.extend(refs)
        else:
            args.append('HEAD')
        
        repo.git.execute(args)
        
        file_size = bundle_path.stat().st_size if bundle_path.exists() else 0
        size_mb = file_size / (1024 * 1024)
        
        print_success(f"Created bundle: {bundle_path}")
        
        panel_content = f"[bold cyan]File:[/bold cyan] {bundle_path}\n"
        panel_content += f"[bold cyan]Size:[/bold cyan] {size_mb:.2f} MB\n"
        panel_content += f"[bold cyan]Refs:[/bold cyan] {', '.join(refs) if refs else 'HEAD'}"
        
        console.print(create_panel(panel_content, "Bundle Created"))
        log_command('bundle create', True, f"Created bundle: {bundle_path}")
        
    except Exception as e:
        print_error(f"Failed to create bundle: {str(e)}")
        log_command('bundle create', False, str(e))

@bundle_cmd.command('verify')
@click.argument('file')
def verify_bundle(file):
    """Verify a bundle file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        bundle_path = Path(file)
        
        if not bundle_path.exists():
            print_error(f"Bundle file not found: {file}")
            return
        
        output = repo.git.bundle('verify', str(bundle_path))
        
        console.print(create_panel(output, "Bundle Verification"))
        print_success("Bundle is valid")
        log_command('bundle verify', True)
        
    except Exception as e:
        print_error(f"Bundle verification failed: {str(e)}")
        log_command('bundle verify', False, str(e))

@bundle_cmd.command('list-heads')
@click.argument('file')
def list_heads(file):
    """List references in a bundle"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        bundle_path = Path(file)
        
        if not bundle_path.exists():
            print_error(f"Bundle file not found: {file}")
            return
        
        output = repo.git.bundle('list-heads', str(bundle_path))
        
        console.print(create_panel(output, f"References in {file}"))
        log_command('bundle list-heads', True)
        
    except Exception as e:
        print_error(f"Failed to list bundle heads: {str(e)}")
        log_command('bundle list-heads', False, str(e))

@bundle_cmd.command('unbundle')
@click.argument('file')
@click.option('--fetch', is_flag=True, help='Fetch from bundle instead of cloning')
def unbundle(file, fetch):
    """Extract/fetch from a bundle file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        bundle_path = Path(file)
        
        if not bundle_path.exists():
            print_error(f"Bundle file not found: {file}")
            return
        
        if fetch:
            repo.git.fetch(str(bundle_path))
            print_success(f"Fetched from bundle: {file}")
        else:
            output = repo.git.bundle('unbundle', str(bundle_path))
            console.print(output)
            print_success(f"Unbundled: {file}")
        
        log_command('bundle unbundle', True, f"Unbundled: {file}")
        
    except Exception as e:
        print_error(f"Failed to unbundle: {str(e)}")
        log_command('bundle unbundle', False, str(e))
