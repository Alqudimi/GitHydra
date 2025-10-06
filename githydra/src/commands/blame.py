"""Git blame command to show line-by-line authorship"""

import click
from githydra.src.ui.console import console, print_success, print_error, print_info, create_table
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.command('blame')
@click.argument('file')
@click.option('--line-start', '-L', type=int, help='Start line number')
@click.option('--line-end', type=int, help='End line number')
@click.option('--commit', '-c', help='Annotate from specific commit')
@click.option('--show-email', '-e', is_flag=True, help='Show author email')
@click.option('--show-stats', '-s', is_flag=True, help='Show statistics')
def blame_cmd(file, line_start, line_end, commit, show_email, show_stats):
    """Show what revision and author last modified each line of a file"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = []
        
        if show_email:
            args.append('-e')
        
        if line_start and line_end:
            args.append(f'-L{line_start},{line_end}')
        elif line_start:
            args.append(f'-L{line_start}')
        
        if commit:
            args.append(commit)
        
        args.append(file)
        
        output = repo.git.blame(*args)
        
        if not output:
            print_info(f"No blame information for '{file}'")
            return
        
        if show_stats:
            lines = output.strip().split('\n')
            authors = {}
            
            for line in lines:
                if '(' in line and ')' in line:
                    author_part = line[line.index('(') + 1:line.index(')')]
                    author = author_part.split()[0]
                    authors[author] = authors.get(author, 0) + 1
            
            table = create_table(f"Blame Statistics for {file}", ["Author", "Lines", "Percentage"])
            total_lines = len(lines)
            
            for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_lines) * 100
                table.add_row(author, str(count), f"{percentage:.1f}%")
            
            console.print(table)
        else:
            console.print(f"[bold cyan]Blame for {file}:[/bold cyan]\n")
            console.print(output)
        
        log_command('blame', True, f"Blamed file: {file}")
        
    except Exception as e:
        print_error(f"Failed to show blame: {str(e)}")
        log_command('blame', False, str(e))
