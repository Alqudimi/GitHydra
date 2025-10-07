from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import defaultdict
import git
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


class TeamAnalytics:
    """Analyze team collaboration and productivity metrics."""
    
    def __init__(self, repo_path: str = "."):
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a valid Git repository: {repo_path}")
    
    def analyze_team(self, days: int = 30) -> Dict[str, Any]:
        """Analyze team performance over specified days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        commits = list(self.repo.iter_commits(since=start_date.isoformat()))
        
        analytics = {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "total_commits": len(commits),
            "authors": self._analyze_authors(commits),
            "activity_by_day": self._analyze_activity_by_day(commits),
            "activity_by_hour": self._analyze_activity_by_hour(commits),
            "collaboration": self._analyze_collaboration(commits),
            "file_ownership": self._analyze_file_ownership(commits)
        }
        
        return analytics
    
    def _analyze_authors(self, commits: List[git.Commit]) -> Dict[str, Any]:
        """Analyze author statistics."""
        author_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "commits": 0,
            "lines_added": 0,
            "lines_deleted": 0,
            "files_changed": set()
        })
        
        for commit in commits:
            author = str(commit.author)
            author_stats[author]["commits"] += 1
            author_stats[author]["lines_added"] += commit.stats.total["insertions"]
            author_stats[author]["lines_deleted"] += commit.stats.total["deletions"]
            files_set = author_stats[author]["files_changed"]
            if isinstance(files_set, set):
                files_set.update(commit.stats.files.keys())
        
        for author in author_stats:
            files_changed = author_stats[author]["files_changed"]
            author_stats[author]["files_changed"] = len(files_changed) if isinstance(files_changed, set) else 0
        
        return dict(author_stats)
    
    def _analyze_activity_by_day(self, commits: List[git.Commit]) -> Dict[str, int]:
        """Analyze commit activity by day of week."""
        activity = defaultdict(int)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for commit in commits:
            day = datetime.fromtimestamp(commit.committed_date).weekday()
            activity[days[day]] += 1
        
        return dict(activity)
    
    def _analyze_activity_by_hour(self, commits: List[git.Commit]) -> Dict[int, int]:
        """Analyze commit activity by hour of day."""
        activity = defaultdict(int)
        
        for commit in commits:
            hour = datetime.fromtimestamp(commit.committed_date).hour
            activity[hour] += 1
        
        return dict(activity)
    
    def _analyze_collaboration(self, commits: List[git.Commit]) -> Dict[str, Any]:
        """Analyze collaboration patterns."""
        file_authors = defaultdict(set)
        
        for commit in commits:
            author = str(commit.author)
            for file in commit.stats.files.keys():
                file_authors[file].add(author)
        
        collaborative_files = {f: list(authors) for f, authors in file_authors.items() if len(authors) > 1}
        
        return {
            "total_files": len(file_authors),
            "collaborative_files": len(collaborative_files),
            "collaboration_rate": len(collaborative_files) / len(file_authors) if file_authors else 0,
            "top_collaborative_files": sorted(
                collaborative_files.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:5]
        }
    
    def _analyze_file_ownership(self, commits: List[git.Commit]) -> Dict[str, str]:
        """Determine primary owner of files based on commits."""
        file_commits = defaultdict(lambda: defaultdict(int))
        
        for commit in commits:
            author = str(commit.author)
            for file in commit.stats.files.keys():
                file_commits[file][author] += 1
        
        ownership = {}
        for file, authors in file_commits.items():
            primary_owner = max(authors.items(), key=lambda x: x[1])
            ownership[file] = primary_owner[0]
        
        return ownership
    
    def display_analytics(self, analytics: Dict[str, Any]):
        """Display team analytics in formatted output."""
        console.print(Panel(
            f"[bold cyan]Team Analytics Report[/bold cyan]\n{analytics['period']}",
            border_style="cyan"
        ))
        
        author_table = Table(title="Author Statistics", box=box.ROUNDED)
        author_table.add_column("Author", style="cyan")
        author_table.add_column("Commits", style="green")
        author_table.add_column("Lines +", style="green")
        author_table.add_column("Lines -", style="red")
        author_table.add_column("Files", style="yellow")
        
        for author, stats in sorted(analytics["authors"].items(), key=lambda x: x[1]["commits"], reverse=True):
            author_table.add_row(
                author,
                str(stats["commits"]),
                str(stats["lines_added"]),
                str(stats["lines_deleted"]),
                str(stats["files_changed"])
            )
        
        console.print(author_table)
        
        day_table = Table(title="Activity by Day", box=box.ROUNDED)
        day_table.add_column("Day", style="cyan")
        day_table.add_column("Commits", style="green")
        
        for day, count in analytics["activity_by_day"].items():
            day_table.add_row(day, str(count))
        
        console.print(day_table)
        
        collab = analytics["collaboration"]
        console.print(Panel(
            f"[bold yellow]Collaboration Metrics[/bold yellow]\n\n" +
            f"Total Files: {collab['total_files']}\n" +
            f"Collaborative Files: {collab['collaborative_files']}\n" +
            f"Collaboration Rate: {collab['collaboration_rate']:.1%}",
            border_style="yellow"
        ))
        
        if collab["top_collaborative_files"]:
            console.print("\n[bold cyan]Most Collaborative Files:[/bold cyan]")
            for file, authors in collab["top_collaborative_files"]:
                console.print(f"  [green]{file}[/green] - {len(authors)} contributors")
