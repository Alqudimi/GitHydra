"""Team Collaboration Commands - Pull Requests, Code Reviews, Contributors"""

import click
import questionary
from pathlib import Path
from datetime import datetime
from githydra.src.ui.console import (
    console, print_success, print_error, print_warning, print_info,
    create_professional_table, create_panel, ICONS, print_section_header,
    show_loading_animation, print_animated_notification
)
from githydra.src.utils.git_helper import get_repo, get_commit_history
from githydra.src.logger import log_command

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

@click.group('team')
def team_cmd():
    """Team collaboration commands"""
    pass

@team_cmd.command('contributors')
def list_contributors():
    """List repository contributors with statistics"""
    try:
        repo = get_repo()
        if not repo:
            return
        
        print_section_header("Repository Contributors", ICONS['star'])
        
        show_loading_animation("Analyzing contributor statistics", 1.5)
        
        contributors = {}
        
        for commit in repo.iter_commits(max_count=200):
            try:
                author = commit.author.name
                email = commit.author.email
                
                if author not in contributors:
                    contributors[author] = {
                        'email': email,
                        'commits': 0,
                        'additions': 0,
                        'deletions': 0,
                        'last_commit': commit.committed_datetime
                    }
                
                contributors[author]['commits'] += 1
                
                stats = commit.stats
                contributors[author]['additions'] += stats.total['insertions']
                contributors[author]['deletions'] += stats.total['deletions']
                
                if commit.committed_datetime > contributors[author]['last_commit']:
                    contributors[author]['last_commit'] = commit.committed_datetime
            except Exception:
                continue
        
        if not contributors:
            print_info("No contributors found")
            return
        
        sorted_contributors = sorted(
            contributors.items(),
            key=lambda x: x[1]['commits'],
            reverse=True
        )
        
        contributors_data = []
        for name, stats in sorted_contributors:
            contributors_data.append((
                name,
                stats['email'],
                str(stats['commits']),
                f"+{stats['additions']}",
                f"-{stats['deletions']}",
                stats['last_commit'].strftime('%Y-%m-%d')
            ))
        
        table = create_professional_table(
            f"{ICONS['star']} Top Contributors",
            [
                ("Name", "bold cyan", "left"),
                ("Email", "yellow", "left"),
                ("Commits", "green", "center"),
                ("Added", "bright_green", "center"),
                ("Removed", "bright_red", "center"),
                ("Last Commit", "magenta", "center")
            ],
            contributors_data,
            show_lines=True,
            caption=f"Total contributors: {len(contributors)}"
        )
        
        console.print(table)
        log_command('team contributors', True)
        
    except Exception as e:
        print_error(f"Failed to list contributors: {str(e)}")
        log_command('team contributors', False, str(e))

@team_cmd.command('activity')
@click.option('--days', '-d', default=30, help='Number of days to analyze')
def show_activity(days):
    """Show team activity for recent days"""
    try:
        repo = get_repo()
        if not repo:
            return
        
        print_section_header(f"Team Activity (Last {days} days)", ICONS['chart'])
        
        show_loading_animation("Analyzing team activity", 1.5)
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        daily_commits = {}
        authors = set()
        
        for commit in repo.iter_commits():
            commit_date = commit.committed_datetime.replace(tzinfo=None)
            
            if commit_date < cutoff_date:
                break
            
            date_key = commit_date.strftime('%Y-%m-%d')
            
            if date_key not in daily_commits:
                daily_commits[date_key] = 0
            
            daily_commits[date_key] += 1
            authors.add(commit.author.name)
        
        total_commits = sum(daily_commits.values())
        avg_commits = total_commits / len(daily_commits) if daily_commits else 0
        
        activity_data = []
        for date in sorted(daily_commits.keys(), reverse=True)[:10]:
            commits = daily_commits[date]
            bar = '█' * min(commits, 20)
            activity_data.append((
                date,
                str(commits),
                bar
            ))
        
        table = create_professional_table(
            f"{ICONS['chart']} Daily Commit Activity",
            [
                ("Date", "bold cyan", "left"),
                ("Commits", "yellow", "center"),
                ("Activity", "green", "left")
            ],
            activity_data,
            show_lines=True
        )
        
        console.print(table)
        
        summary = {
            'Total Commits': str(total_commits),
            'Active Contributors': str(len(authors)),
            'Average Commits/Day': f"{avg_commits:.1f}",
            'Period': f"{days} days"
        }
        
        console.print(create_panel(
            "\n".join([f"[bold cyan]{k}:[/bold cyan] [white]{v}[/white]" for k, v in summary.items()]),
            f"{ICONS['info']} Activity Summary",
            "cyan"
        ))
        
        log_command('team activity', True)
        
    except Exception as e:
        print_error(f"Failed to show team activity: {str(e)}")
        log_command('team activity', False, str(e))

@team_cmd.command('pr-list')
@click.option('--repo', '-r', help='Repository name (owner/repo)')
@click.option('--state', '-s', default='open', type=click.Choice(['open', 'closed', 'all']))
def list_pull_requests(repo, state):
    """List GitHub pull requests"""
    try:
        if not GITHUB_AVAILABLE:
            print_error("PyGithub is not installed. Run: pip install PyGithub")
            return
        
        token_file = Path.home() / '.githydra' / 'github_token'
        if not token_file.exists():
            print_error("Not connected to GitHub. Use 'githydra cloud connect-github' first")
            return
        
        if not repo:
            repo = questionary.text(
                f"{ICONS['arrow']} Enter repository (owner/repo):",
                validate=lambda x: '/' in x or "Format: owner/repo"
            ).ask()
            
            if not repo:
                return
        
        token = token_file.read_text().strip()
        g = Github(token)
        
        show_loading_animation(f"Fetching pull requests from {repo}", 1.0)
        
        gh_repo = g.get_repo(repo)
        prs = gh_repo.get_pulls(state=state)
        
        pr_data = []
        for pr in list(prs)[:20]:
            status_icon = '✅' if pr.merged else ('🔀' if state == 'open' else '❌')
            pr_data.append((
                f"#{pr.number}",
                pr.title[:45] + ('...' if len(pr.title) > 45 else ''),
                f"{status_icon} {pr.state.upper()}",
                pr.user.login,
                str(pr.comments),
                pr.created_at.strftime('%Y-%m-%d')
            ))
        
        table = create_professional_table(
            f"{ICONS['merge']} Pull Requests: {repo}",
            [
                ("ID", "bold yellow", "center"),
                ("Title", "cyan", "left"),
                ("Status", "green", "center"),
                ("Author", "magenta", "left"),
                ("Comments", "blue", "center"),
                ("Created", "yellow", "center")
            ],
            pr_data,
            show_lines=True,
            caption=f"Showing {state} pull requests"
        )
        
        console.print(table)
        log_command('team pr-list', True, f"Repo: {repo}")
        
    except Exception as e:
        print_error(f"Failed to list pull requests: {str(e)}")
        log_command('team pr-list', False, str(e))

@team_cmd.command('review')
@click.option('--branch', '-b', help='Branch to review')
def review_branch(branch):
    """Review changes in a branch"""
    try:
        repo = get_repo()
        if not repo:
            return
        
        if not branch:
            branches = [b.name for b in repo.branches]
            branch = questionary.select(
                f"{ICONS['arrow']} Select branch to review:",
                choices=branches
            ).ask()
            
            if not branch:
                return
        
        print_section_header(f"Code Review: {branch}", ICONS['magnify'])
        
        show_loading_animation("Analyzing branch changes", 1.0)
        
        current_branch = repo.active_branch.name
        
        diff = repo.git.diff(f"{current_branch}...{branch}", stat=True)
        
        if not diff:
            print_info(f"No differences between {current_branch} and {branch}")
            return
        
        console.print(create_panel(
            diff,
            f"{ICONS['file']} Branch Comparison",
            "cyan"
        ))
        
        commits = list(repo.iter_commits(f"{current_branch}..{branch}"))
        
        if commits:
            commit_data = []
            for commit in commits[:10]:
                commit_data.append((
                    commit.hexsha[:7],
                    commit.author.name,
                    commit.message.split('\n')[0][:50],
                    commit.committed_datetime.strftime('%Y-%m-%d %H:%M')
                ))
            
            table = create_professional_table(
                f"{ICONS['commit']} New Commits in {branch}",
                [
                    ("Hash", "yellow", "left"),
                    ("Author", "cyan", "left"),
                    ("Message", "white", "left"),
                    ("Date", "magenta", "center")
                ],
                commit_data,
                show_lines=True
            )
            
            console.print(table)
        
        log_command('team review', True, f"Branch: {branch}")
        
    except Exception as e:
        print_error(f"Failed to review branch: {str(e)}")
        log_command('team review', False, str(e))

@team_cmd.command('workflow')
def show_workflow():
    """Display team collaboration workflow guide"""
    try:
        print_section_header("Team Collaboration Workflow", ICONS['sparkles'])
        
        workflow_steps = [
            (f"{ICONS['branch']}", "Create feature branch", "cyan"),
            (f"{ICONS['commit']}", "Make commits with clear messages", "cyan"),
            (f"{ICONS['upload']}", "Push branch to remote", "cyan"),
            (f"{ICONS['merge']}", "Create pull request", "cyan"),
            (f"{ICONS['magnify']}", "Code review by team", "cyan"),
            (f"{ICONS['check']}", "Merge to main branch", "green"),
        ]
        
        workflow_content = create_colorful_list(workflow_steps, "Recommended Workflow:")
        
        console.print(create_panel(
            workflow_content,
            f"{ICONS['rocket']} Git Team Workflow",
            "bright_cyan"
        ))
        
        best_practices = [
            (f"{ICONS['star']}", "Write descriptive commit messages", "yellow"),
            (f"{ICONS['star']}", "Review code before merging", "yellow"),
            (f"{ICONS['star']}", "Keep branches up to date", "yellow"),
            (f"{ICONS['star']}", "Use meaningful branch names", "yellow"),
            (f"{ICONS['star']}", "Test before pushing", "yellow"),
        ]
        
        practices_content = create_colorful_list(best_practices, "Best Practices:")
        
        console.print(create_panel(
            practices_content,
            f"{ICONS['shield']} Team Best Practices",
            "bright_magenta"
        ))
        
        log_command('team workflow', True)
        
    except Exception as e:
        print_error(f"Failed to show workflow: {str(e)}")
        log_command('team workflow', False, str(e))
