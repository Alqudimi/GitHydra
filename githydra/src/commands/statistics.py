"""Repository statistics and analytics commands"""

import click
from datetime import datetime, timedelta
from collections import defaultdict
from githydra.src.ui.console import console, print_success, print_error, print_info, create_table, create_panel
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

@click.group('stats')
def stats_cmd():
    """Repository statistics and analytics"""
    pass

@stats_cmd.command('overview')
def stats_overview():
    """Show repository overview statistics"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        total_commits = len(list(repo.iter_commits()))
        
        branches = len(list(repo.branches))
        
        tags = len(list(repo.tags))
        
        remotes = len(list(repo.remotes))
        
        try:
            contributors = len(set(commit.author.name for commit in repo.iter_commits()))
        except:
            contributors = 0
        
        try:
            first_commit = list(repo.iter_commits())[-1]
            repo_age = (datetime.now() - first_commit.committed_datetime.replace(tzinfo=None)).days
        except:
            repo_age = 0
        
        panel_content = f"[bold cyan]Total Commits:[/bold cyan] {total_commits}\n"
        panel_content += f"[bold cyan]Branches:[/bold cyan] {branches}\n"
        panel_content += f"[bold cyan]Tags:[/bold cyan] {tags}\n"
        panel_content += f"[bold cyan]Remotes:[/bold cyan] {remotes}\n"
        panel_content += f"[bold cyan]Contributors:[/bold cyan] {contributors}\n"
        panel_content += f"[bold cyan]Repository Age:[/bold cyan] {repo_age} days"
        
        console.print(create_panel(panel_content, "Repository Overview"))
        log_command('stats overview', True)
        
    except Exception as e:
        print_error(f"Failed to generate overview: {str(e)}")
        log_command('stats overview', False, str(e))

@stats_cmd.command('contributors')
@click.option('--limit', '-n', default=10, type=int, help='Number of top contributors to show')
@click.option('--since', help='Count commits since date (e.g., "1 month ago")')
def stats_contributors(limit, since):
    """Show contributor statistics"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        author_stats = defaultdict(lambda: {'commits': 0, 'lines_added': 0, 'lines_deleted': 0})
        
        args = []
        if since:
            args.append(f'--since={since}')
        
        for commit in repo.iter_commits(*args):
            author = commit.author.name
            author_stats[author]['commits'] += 1
            
            try:
                stats = commit.stats.total
                author_stats[author]['lines_added'] += stats.get('insertions', 0)
                author_stats[author]['lines_deleted'] += stats.get('deletions', 0)
            except:
                pass
        
        sorted_authors = sorted(author_stats.items(), key=lambda x: x[1]['commits'], reverse=True)
        
        table = create_table("Top Contributors", ["Author", "Commits", "Lines +", "Lines -", "Total Changes"])
        
        for author, stats in sorted_authors[:limit]:
            total_changes = stats['lines_added'] + stats['lines_deleted']
            table.add_row(
                author,
                str(stats['commits']),
                f"[green]+{stats['lines_added']}[/green]",
                f"[red]-{stats['lines_deleted']}[/red]",
                str(total_changes)
            )
        
        console.print(table)
        log_command('stats contributors', True)
        
    except Exception as e:
        print_error(f"Failed to generate contributor stats: {str(e)}")
        log_command('stats contributors', False, str(e))

@stats_cmd.command('activity')
@click.option('--days', '-d', default=30, type=int, help='Number of days to analyze')
def stats_activity(days):
    """Show commit activity over time"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        since_date = datetime.now() - timedelta(days=days)
        
        daily_commits = defaultdict(int)
        hourly_commits = defaultdict(int)
        weekday_commits = defaultdict(int)
        
        for commit in repo.iter_commits(since=since_date):
            commit_date = commit.committed_datetime.replace(tzinfo=None)
            day_key = commit_date.strftime('%Y-%m-%d')
            hour_key = commit_date.hour
            weekday_key = commit_date.strftime('%A')
            
            daily_commits[day_key] += 1
            hourly_commits[hour_key] += 1
            weekday_commits[weekday_key] += 1
        
        console.print(f"[bold cyan]Commit Activity (Last {days} Days)[/bold cyan]\n")
        
        table = create_table("Daily Activity", ["Date", "Commits"])
        for date in sorted(daily_commits.keys(), reverse=True)[:10]:
            table.add_row(date, str(daily_commits[date]))
        console.print(table)
        
        console.print("\n[bold cyan]Commits by Hour of Day:[/bold cyan]")
        for hour in range(24):
            count = hourly_commits.get(hour, 0)
            bar = '█' * count
            console.print(f"{hour:02d}:00  {bar} ({count})")
        
        console.print("\n")
        table = create_table("Commits by Weekday", ["Day", "Commits"])
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in weekdays:
            table.add_row(day, str(weekday_commits.get(day, 0)))
        console.print(table)
        
        log_command('stats activity', True)
        
    except Exception as e:
        print_error(f"Failed to generate activity stats: {str(e)}")
        log_command('stats activity', False, str(e))

@stats_cmd.command('files')
@click.option('--limit', '-n', default=10, type=int, help='Number of files to show')
def stats_files(limit):
    """Show file change statistics"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        file_stats = defaultdict(lambda: {'changes': 0, 'additions': 0, 'deletions': 0})
        
        for commit in repo.iter_commits():
            try:
                for file, stats in commit.stats.files.items():
                    file_stats[file]['changes'] += 1
                    file_stats[file]['additions'] += stats.get('insertions', 0)
                    file_stats[file]['deletions'] += stats.get('deletions', 0)
            except:
                pass
        
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1]['changes'], reverse=True)
        
        table = create_table(
            "Most Modified Files",
            ["File", "Changes", "Lines +", "Lines -", "Total"]
        )
        
        for file, stats in sorted_files[:limit]:
            total = stats['additions'] + stats['deletions']
            table.add_row(
                file[:50],
                str(stats['changes']),
                f"[green]+{stats['additions']}[/green]",
                f"[red]-{stats['deletions']}[/red]",
                str(total)
            )
        
        console.print(table)
        log_command('stats files', True)
        
    except Exception as e:
        print_error(f"Failed to generate file stats: {str(e)}")
        log_command('stats files', False, str(e))

@stats_cmd.command('languages')
def stats_languages():
    """Analyze programming languages in repository"""
    repo = get_repo()
    if not repo:
        return
    
    try:
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': '.C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.html': 'HTML',
            '.css': 'CSS',
            '.sh': 'Shell',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
        }
        
        language_lines = defaultdict(int)
        
        try:
            from pathlib import Path
            repo_path = Path(repo.working_dir)
            
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                    ext = file_path.suffix.lower()
                    if ext in language_extensions:
                        try:
                            lines = len(file_path.read_text(errors='ignore').splitlines())
                            language_lines[language_extensions[ext]] += lines
                        except:
                            pass
        except:
            print_error("Could not analyze repository files")
            return
        
        if not language_lines:
            print_info("No recognized programming language files found")
            return
        
        total_lines = sum(language_lines.values())
        sorted_languages = sorted(language_lines.items(), key=lambda x: x[1], reverse=True)
        
        table = create_table("Programming Languages", ["Language", "Lines", "Percentage"])
        
        for language, lines in sorted_languages:
            percentage = (lines / total_lines) * 100
            bar = '█' * int(percentage / 2)
            table.add_row(
                language,
                str(lines),
                f"{percentage:.1f}% {bar}"
            )
        
        console.print(table)
        console.print(f"\n[bold cyan]Total Lines:[/bold cyan] {total_lines}")
        
        log_command('stats languages', True)
        
    except Exception as e:
        print_error(f"Failed to analyze languages: {str(e)}")
        log_command('stats languages', False, str(e))
