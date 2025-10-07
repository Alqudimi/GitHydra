from datetime import datetime, timedelta
from typing import Dict, Any, List
import git
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from githydra.src.ai_service import ai_service

console = Console()


class WeeklyReport:
    """Generate weekly Git repository reports."""
    
    def __init__(self, repo_path: str = "."):
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a valid Git repository: {repo_path}")
    
    def generate_report(self, weeks: int = 1) -> Dict[str, Any]:
        """Generate weekly report for specified number of weeks."""
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        commits = self._get_commits_in_range(start_date, end_date)
        
        report = {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "total_commits": len(commits),
            "contributors": self._get_contributors(commits),
            "files_changed": self._get_files_changed(commits),
            "lines_stats": self._get_lines_stats(commits),
            "commits": commits,
            "ai_summary": None
        }
        
        if ai_service.is_enabled():
            report["ai_summary"] = ai_service.summarize_changes(commits)
        
        return report
    
    def _get_commits_in_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get commits within date range."""
        commits = []
        
        try:
            for commit in self.repo.iter_commits():
                commit_date = datetime.fromtimestamp(commit.committed_date)
                
                if start_date <= commit_date <= end_date:
                    commits.append({
                        "sha": commit.hexsha[:7],
                        "author": str(commit.author),
                        "date": commit_date.strftime('%Y-%m-%d %H:%M'),
                        "message": commit.message.split('\n')[0],
                        "files_changed": len(commit.stats.files)
                    })
                elif commit_date < start_date:
                    break
        except Exception as e:
            console.print(f"[red]Error getting commits: {e}[/red]")
        
        return commits
    
    def _get_contributors(self, commits: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get contributor statistics."""
        contributors = {}
        for commit in commits:
            author = commit["author"]
            contributors[author] = contributors.get(author, 0) + 1
        return contributors
    
    def _get_files_changed(self, commits: List[Dict[str, Any]]) -> int:
        """Get total files changed."""
        return sum(c["files_changed"] for c in commits)
    
    def _get_lines_stats(self, commits: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get lines added/deleted statistics."""
        try:
            stats = {"added": 0, "deleted": 0}
            for commit in commits:
                commit_obj = self.repo.commit(commit["sha"])
                stats["added"] += commit_obj.stats.total["insertions"]
                stats["deleted"] += commit_obj.stats.total["deletions"]
            return stats
        except:
            return {"added": 0, "deleted": 0}
    
    def display_report(self, report: Dict[str, Any]):
        """Display formatted report in terminal."""
        console.print(Panel(
            f"[bold cyan]Weekly Git Report[/bold cyan]\n{report['period']}",
            border_style="cyan"
        ))
        
        table = Table(title="Summary", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Commits", str(report["total_commits"]))
        table.add_row("Files Changed", str(report["files_changed"]))
        table.add_row("Lines Added", str(report["lines_stats"]["added"]))
        table.add_row("Lines Deleted", str(report["lines_stats"]["deleted"]))
        table.add_row("Contributors", str(len(report["contributors"])))
        
        console.print(table)
        
        if report["contributors"]:
            contrib_table = Table(title="Contributors", show_header=True)
            contrib_table.add_column("Author", style="cyan")
            contrib_table.add_column("Commits", style="green")
            
            for author, count in sorted(report["contributors"].items(), key=lambda x: x[1], reverse=True):
                contrib_table.add_row(author, str(count))
            
            console.print(contrib_table)
        
        if report.get("ai_summary"):
            console.print(Panel(
                f"[bold yellow]AI-Generated Insights[/bold yellow]\n\n{report['ai_summary']}",
                border_style="yellow"
            ))
        
        if report["commits"]:
            console.print("\n[bold cyan]Recent Commits:[/bold cyan]")
            for commit in report["commits"][:10]:
                console.print(f"  [green]{commit['sha']}[/green] {commit['message']} - [dim]{commit['author']}[/dim]")
