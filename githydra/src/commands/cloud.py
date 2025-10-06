"""Cloud Integration Commands - GitHub, GitLab, and Cloud Backup"""

import click
import questionary
from pathlib import Path
from githydra.src.ui.console import (
    console, print_success, print_error, print_warning, print_info,
    create_professional_table, create_panel, ICONS, print_section_header,
    show_loading_animation, print_animated_notification
)
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

@click.group('cloud')
def cloud_cmd():
    """Cloud integration commands for GitHub, GitLab, and backups"""
    pass

@cloud_cmd.command('connect-github')
@click.option('--token', '-t', help='GitHub personal access token')
def connect_github(token):
    """Connect to GitHub with authentication"""
    try:
        if not GITHUB_AVAILABLE:
            print_error("PyGithub is not installed. Run: pip install PyGithub")
            return
        
        if not token:
            token = questionary.password(
                f"{ICONS['shield']} Enter GitHub Personal Access Token:",
                validate=lambda x: len(x) > 0 or "Token cannot be empty"
            ).ask()
            
            if not token:
                print_error("Authentication cancelled")
                return
        
        show_loading_animation("Connecting to GitHub", 1.5)
        
        try:
            g = Github(token)
            user = g.get_user()
            
            config_dir = Path.home() / '.githydra'
            config_dir.mkdir(exist_ok=True)
            
            with open(config_dir / 'github_token', 'w') as f:
                f.write(token)
            
            info_data = {
                'Username': user.login,
                'Name': user.name or 'N/A',
                'Email': user.email or 'N/A',
                'Public Repos': str(user.public_repos),
                'Followers': str(user.followers),
            }
            
            console.print(create_panel(
                "\n".join([f"[bold cyan]{k}:[/bold cyan] [white]{v}[/white]" for k, v in info_data.items()]),
                f"{ICONS['success']} Connected to GitHub Successfully",
                "green"
            ))
            
            print_success("GitHub token saved to ~/.githydra/github_token")
            log_command('cloud connect-github', True, f"User: {user.login}")
            
        except GithubException as e:
            print_error(f"GitHub authentication failed: {str(e)}")
            log_command('cloud connect-github', False, str(e))
        
    except Exception as e:
        print_error(f"Failed to connect to GitHub: {str(e)}")
        log_command('cloud connect-github', False, str(e))

@cloud_cmd.command('repos')
@click.option('--limit', '-l', default=10, help='Number of repositories to show')
def list_repos(limit):
    """List your GitHub repositories"""
    try:
        if not GITHUB_AVAILABLE:
            print_error("PyGithub is not installed. Run: pip install PyGithub")
            return
        
        token_file = Path.home() / '.githydra' / 'github_token'
        if not token_file.exists():
            print_error("Not connected to GitHub. Use 'githydra cloud connect-github' first")
            return
        
        token = token_file.read_text().strip()
        
        show_loading_animation("Fetching repositories from GitHub", 1.0)
        
        g = Github(token)
        user = g.get_user()
        
        repos_data = []
        for repo in user.get_repos()[:limit]:
            repos_data.append((
                repo.name,
                f"{'⭐' if repo.private else '🌐'} {repo.language or 'N/A'}",
                str(repo.stargazers_count),
                str(repo.forks_count),
                repo.updated_at.strftime('%Y-%m-%d')
            ))
        
        table = create_professional_table(
            f"{ICONS['git']} Your GitHub Repositories",
            [
                ("Repository", "bold cyan", "left"),
                ("Type & Language", "yellow", "left"),
                ("Stars", "green", "center"),
                ("Forks", "blue", "center"),
                ("Updated", "magenta", "center")
            ],
            repos_data,
            show_lines=True,
            caption=f"Showing {len(repos_data)} of {user.public_repos + user.total_private_repos} repositories"
        )
        
        console.print(table)
        log_command('cloud repos', True)
        
    except Exception as e:
        print_error(f"Failed to list repositories: {str(e)}")
        log_command('cloud repos', False, str(e))

@cloud_cmd.command('sync')
@click.option('--repo', '-r', help='Repository name (owner/repo)')
def sync_repo(repo):
    """Sync local repository with GitHub"""
    try:
        local_repo = get_repo()
        if not local_repo:
            return
        
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
                print_error("Sync cancelled")
                return
        
        token = token_file.read_text().strip()
        g = Github(token)
        
        show_loading_animation(f"Syncing with {repo}", 1.5)
        
        gh_repo = g.get_repo(repo)
        
        print_info(f"Repository: {gh_repo.full_name}")
        print_info(f"Description: {gh_repo.description or 'N/A'}")
        
        local_repo.git.fetch('origin')
        print_success("Fetched latest changes from remote")
        
        local_repo.git.pull('origin', local_repo.active_branch.name)
        print_success(f"Pulled changes to {local_repo.active_branch.name}")
        
        print_animated_notification("Repository synchronized successfully", "success", 1.0)
        log_command('cloud sync', True, f"Repo: {repo}")
        
    except Exception as e:
        print_error(f"Failed to sync repository: {str(e)}")
        log_command('cloud sync', False, str(e))

@cloud_cmd.command('backup')
@click.option('--output', '-o', help='Backup output directory')
def backup_repo(output):
    """Create a backup of the current repository"""
    try:
        repo = get_repo()
        if not repo:
            return
        
        if not output:
            output = questionary.text(
                f"{ICONS['arrow']} Backup directory path:",
                default=f"./backup_{Path.cwd().name}"
            ).ask()
            
            if not output:
                print_error("Backup cancelled")
                return
        
        output_path = Path(output).absolute()
        current_path = Path.cwd().absolute()
        
        print_section_header("Repository Backup", ICONS['save'])
        
        show_loading_animation("Creating repository backup", 2.0)
        
        import shutil
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        shutil.copytree('.git', output_path / '.git', dirs_exist_ok=True)
        
        for file in Path('.').rglob('*'):
            file_abs = file.absolute()
            
            if file_abs == output_path or output_path in file_abs.parents:
                continue
            
            if file.is_file() and '.git' not in str(file):
                try:
                    dest = output_path / file
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, dest)
                except Exception:
                    pass
        
        backup_info = {
            'Location': str(output_path.absolute()),
            'Repository': Path.cwd().name,
            'Branch': repo.active_branch.name,
            'Commits': str(repo.head.commit.count()),
            'Size': f"{sum(f.stat().st_size for f in output_path.rglob('*') if f.is_file()) / 1024 / 1024:.2f} MB"
        }
        
        console.print(create_panel(
            "\n".join([f"[bold cyan]{k}:[/bold cyan] [white]{v}[/white]" for k, v in backup_info.items()]),
            f"{ICONS['success']} Backup Created Successfully",
            "green"
        ))
        
        log_command('cloud backup', True, f"Output: {output}")
        
    except Exception as e:
        print_error(f"Failed to create backup: {str(e)}")
        log_command('cloud backup', False, str(e))

@cloud_cmd.command('issues')
@click.option('--repo', '-r', help='Repository name (owner/repo)')
@click.option('--state', '-s', default='open', type=click.Choice(['open', 'closed', 'all']))
def list_issues(repo, state):
    """List GitHub issues for a repository"""
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
        
        show_loading_animation(f"Fetching issues from {repo}", 1.0)
        
        gh_repo = g.get_repo(repo)
        issues = gh_repo.get_issues(state=state)
        
        issues_data = []
        for issue in list(issues)[:20]:
            issues_data.append((
                f"#{issue.number}",
                issue.title[:50] + ('...' if len(issue.title) > 50 else ''),
                issue.state,
                issue.user.login,
                str(issue.comments)
            ))
        
        table = create_professional_table(
            f"{ICONS['file']} Issues: {repo}",
            [
                ("ID", "bold yellow", "center"),
                ("Title", "cyan", "left"),
                ("State", "green", "center"),
                ("Author", "magenta", "left"),
                ("Comments", "blue", "center")
            ],
            issues_data,
            show_lines=True,
            caption=f"Showing {state} issues"
        )
        
        console.print(table)
        log_command('cloud issues', True, f"Repo: {repo}")
        
    except Exception as e:
        print_error(f"Failed to list issues: {str(e)}")
        log_command('cloud issues', False, str(e))

@cloud_cmd.command('releases')
@click.option('--repo', '-r', help='Repository name (owner/repo)')
def list_releases(repo):
    """List GitHub releases for a repository"""
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
        
        show_loading_animation(f"Fetching releases from {repo}", 1.0)
        
        gh_repo = g.get_repo(repo)
        releases = gh_repo.get_releases()
        
        releases_data = []
        for release in list(releases)[:10]:
            releases_data.append((
                release.tag_name,
                release.title or 'N/A',
                '✓' if release.prerelease else '✗',
                str(release.get_assets().totalCount),
                release.published_at.strftime('%Y-%m-%d')
            ))
        
        table = create_professional_table(
            f"{ICONS['tag']} Releases: {repo}",
            [
                ("Tag", "bold yellow", "left"),
                ("Title", "cyan", "left"),
                ("Pre-release", "green", "center"),
                ("Assets", "blue", "center"),
                ("Published", "magenta", "center")
            ],
            releases_data,
            show_lines=True
        )
        
        console.print(table)
        log_command('cloud releases', True, f"Repo: {repo}")
        
    except Exception as e:
        print_error(f"Failed to list releases: {str(e)}")
        log_command('cloud releases', False, str(e))
