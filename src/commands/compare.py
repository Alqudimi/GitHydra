"""Branch and commit comparison commands"""

import click
from src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from src.utils.git_helper import get_repo
from src.logger import log_command

@click.group('compare')
def compare_cmd():
    """Compare branches, commits, and tags"""
    pass

@compare_cmd.command('branches')
@click.argument('branch1')
@click.argument('branch2')
@click.option('--stat', is_flag=True, help='Show diffstat')
@click.option('--name-only', is_flag=True, help='Show only file names')
def compare_branches(branch1, branch2, stat, name_only):
    """Compare two branches"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        commits_ahead = list(repo.iter_commits(f'{branch2}..{branch1}'))
        commits_behind = list(repo.iter_commits(f'{branch1}..{branch2}'))
        
        panel_content = f"[bold cyan]Comparing:[/bold cyan] {branch1} ↔ {branch2}\n\n"
        panel_content += f"[bold green]Commits ahead:[/bold green] {len(commits_ahead)}\n"
        panel_content += f"[bold red]Commits behind:[/bold red] {len(commits_behind)}\n"
        
        console.print(create_panel(panel_content, "Branch Comparison"))
        
        if commits_ahead:
            console.print(f"\n[bold green]{branch1} has these commits that {branch2} doesn't:[/bold green]")
            for commit in commits_ahead[:10]:
                console.print(f"  [yellow]{commit.hexsha[:7]}[/yellow] {commit.message.strip()[:60]}")
            if len(commits_ahead) > 10:
                console.print(f"  ... and {len(commits_ahead) - 10} more")
        
        if commits_behind:
            console.print(f"\n[bold red]{branch2} has these commits that {branch1} doesn't:[/bold red]")
            for commit in commits_behind[:10]:
                console.print(f"  [yellow]{commit.hexsha[:7]}[/yellow] {commit.message.strip()[:60]}")
            if len(commits_behind) > 10:
                console.print(f"  ... and {len(commits_behind) - 10} more")
        
        args = ['diff']
        if stat:
            args.append('--stat')
        elif name_only:
            args.append('--name-only')
        
        args.append(f'{branch2}...{branch1}')
        
        diff_output = repo.git.execute(args)
        if diff_output:
            console.print(f"\n[bold cyan]File Differences:[/bold cyan]")
            console.print(diff_output)
        
        log_command('compare branches', True, f"Compared {branch1} and {branch2}")
        
    except Exception as e:
        print_error(f"Failed to compare branches: {str(e)}")
        log_command('compare branches', False, str(e))

@compare_cmd.command('commits')
@click.argument('commit1')
@click.argument('commit2')
@click.option('--stat', is_flag=True, help='Show diffstat')
@click.option('--patch', is_flag=True, help='Show full diff')
def compare_commits(commit1, commit2, stat, patch):
    """Compare two commits"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        args = ['diff']
        
        if stat:
            args.append('--stat')
        elif patch:
            args.append('--patch')
        else:
            args.append('--name-status')
        
        args.extend([commit1, commit2])
        
        output = repo.git.execute(args)
        
        console.print(create_panel(output, f"Comparing {commit1[:7]} → {commit2[:7]}"))
        log_command('compare commits', True, f"Compared {commit1} and {commit2}")
        
    except Exception as e:
        print_error(f"Failed to compare commits: {str(e)}")
        log_command('compare commits', False, str(e))

@compare_cmd.command('files')
@click.argument('file')
@click.option('--branch1', default='HEAD', help='First branch/commit')
@click.option('--branch2', required=True, help='Second branch/commit')
def compare_file(file, branch1, branch2):
    """Compare a specific file between branches"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.diff(branch1, branch2, '--', file)
        
        if not output:
            print_info(f"No differences in '{file}' between {branch1} and {branch2}")
            return
        
        console.print(create_panel(output, f"File: {file} ({branch1} → {branch2})"))
        log_command('compare files', True, f"Compared {file}")
        
    except Exception as e:
        print_error(f"Failed to compare file: {str(e)}")
        log_command('compare files', False, str(e))

@compare_cmd.command('with-remote')
@click.option('--branch', '-b', help='Local branch to compare')
@click.option('--remote', '-r', default='origin', help='Remote name')
def compare_with_remote(branch, remote):
    """Compare local branch with its remote counterpart"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        if not branch:
            branch = repo.active_branch.name
        
        local_ref = branch
        remote_ref = f'{remote}/{branch}'
        
        try:
            commits_ahead = list(repo.iter_commits(f'{remote_ref}..{local_ref}'))
            commits_behind = list(repo.iter_commits(f'{local_ref}..{remote_ref}'))
        except:
            print_error(f"Could not find remote branch '{remote_ref}'")
            return
        
        panel_content = f"[bold cyan]Local:[/bold cyan] {branch}\n"
        panel_content += f"[bold cyan]Remote:[/bold cyan] {remote_ref}\n\n"
        panel_content += f"[bold green]Commits ahead:[/bold green] {len(commits_ahead)}\n"
        panel_content += f"[bold red]Commits behind:[/bold red] {len(commits_behind)}\n\n"
        
        if len(commits_ahead) == 0 and len(commits_behind) == 0:
            panel_content += "[bold green]✓ Up to date with remote[/bold green]"
        elif len(commits_ahead) > 0 and len(commits_behind) == 0:
            panel_content += "[bold yellow]→ Ready to push[/bold yellow]"
        elif len(commits_ahead) == 0 and len(commits_behind) > 0:
            panel_content += "[bold yellow]← Need to pull[/bold yellow]"
        else:
            panel_content += "[bold yellow]↔ Diverged (need to pull and push)[/bold yellow]"
        
        console.print(create_panel(panel_content, "Local vs Remote"))
        
        if commits_ahead:
            console.print(f"\n[bold green]Unpushed commits:[/bold green]")
            for commit in commits_ahead[:5]:
                console.print(f"  [yellow]{commit.hexsha[:7]}[/yellow] {commit.message.strip()[:60]}")
        
        if commits_behind:
            console.print(f"\n[bold red]Commits from remote:[/bold red]")
            for commit in commits_behind[:5]:
                console.print(f"  [yellow]{commit.hexsha[:7]}[/yellow] {commit.message.strip()[:60]}")
        
        log_command('compare with-remote', True, f"Compared {branch} with {remote_ref}")
        
    except Exception as e:
        print_error(f"Failed to compare with remote: {str(e)}")
        log_command('compare with-remote', False, str(e))

@compare_cmd.command('stats')
@click.argument('ref1')
@click.argument('ref2')
def compare_stats(ref1, ref2):
    """Show detailed statistics between two refs"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        output = repo.git.diff('--stat', ref1, ref2)
        
        if not output:
            print_info(f"No differences between {ref1} and {ref2}")
            return
        
        console.print(create_panel(output, f"Statistics: {ref1} → {ref2}"))
        
        shortstat = repo.git.diff('--shortstat', ref1, ref2)
        console.print(f"\n[bold cyan]Summary:[/bold cyan] {shortstat}")
        
        log_command('compare stats', True)
        
    except Exception as e:
        print_error(f"Failed to show comparison stats: {str(e)}")
        log_command('compare stats', False, str(e))
