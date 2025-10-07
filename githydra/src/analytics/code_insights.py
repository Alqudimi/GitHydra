import os
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
import git
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from githydra.src.ai_service import ai_service

console = Console()


class CodeInsights:
    """Analyze code quality, complexity, and patterns."""
    
    def __init__(self, repo_path: str = "."):
        try:
            self.repo = git.Repo(repo_path)
            self.repo_path = Path(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a valid Git repository: {repo_path}")
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Comprehensive repository code analysis."""
        insights = {
            "language_stats": self._analyze_languages(),
            "file_stats": self._analyze_files(),
            "complexity_metrics": self._analyze_complexity(),
            "hotspots": self._identify_hotspots(),
            "code_quality": []
        }
        
        if ai_service.is_enabled():
            insights["code_quality"] = self._ai_code_quality_check()
        
        return insights
    
    def _analyze_languages(self) -> Dict[str, Dict[str, Any]]:
        """Analyze language distribution in repository."""
        lang_stats = defaultdict(lambda: {"files": 0, "lines": 0})
        
        extensions = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".java": "Java", ".cpp": "C++", ".c": "C", ".go": "Go",
            ".rs": "Rust", ".rb": "Ruby", ".php": "PHP", ".cs": "C#",
            ".swift": "Swift", ".kt": "Kotlin", ".html": "HTML",
            ".css": "CSS", ".scss": "SCSS", ".json": "JSON",
            ".yml": "YAML", ".yaml": "YAML", ".md": "Markdown"
        }
        
        for root, _, files in os.walk(self.repo_path):
            if '.git' in root:
                continue
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in extensions:
                    lang = extensions[ext]
                    lang_stats[lang]["files"] += 1
                    
                    try:
                        file_path = Path(root) / file
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            lang_stats[lang]["lines"] += lines
                    except:
                        pass
        
        return dict(lang_stats)
    
    def _analyze_files(self) -> Dict[str, Any]:
        """Analyze file statistics."""
        total_files = 0
        total_lines = 0
        largest_files = []
        
        for root, _, files in os.walk(self.repo_path):
            if '.git' in root:
                continue
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs')):
                    total_files += 1
                    file_path = Path(root) / file
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            total_lines += lines
                            largest_files.append((str(file_path.relative_to(self.repo_path)), lines))
                    except:
                        pass
        
        largest_files.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "average_lines_per_file": total_lines // total_files if total_files > 0 else 0,
            "largest_files": largest_files[:10]
        }
    
    def _analyze_complexity(self) -> Dict[str, Any]:
        """Analyze code complexity metrics."""
        complexity = {
            "large_files": [],
            "deep_nesting_potential": 0,
            "long_functions_potential": 0
        }
        
        for root, _, files in os.walk(self.repo_path):
            if '.git' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            if len(lines) > 500:
                                complexity["large_files"].append(
                                    str(file_path.relative_to(self.repo_path))
                                )
                    except:
                        pass
        
        return complexity
    
    def _identify_hotspots(self) -> List[Dict[str, Any]]:
        """Identify code hotspots (frequently changed files)."""
        file_changes = defaultdict(int)
        
        try:
            for commit in list(self.repo.iter_commits(max_count=200)):
                for file in commit.stats.files.keys():
                    file_changes[file] += 1
        except:
            pass
        
        hotspots = [
            {"file": file, "changes": count}
            for file, count in sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        return hotspots
    
    def _ai_code_quality_check(self) -> List[Dict[str, Any]]:
        """AI-powered code quality check on key files."""
        quality_reports = []
        
        try:
            for root, _, files in os.walk(self.repo_path):
                if '.git' in root or len(quality_reports) >= 5:
                    break
                
                for file in files:
                    if file.endswith('.py') and len(quality_reports) < 5:
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                code = f.read()
                                if len(code) > 100:
                                    review = ai_service.review_code(code, str(file_path.name))
                                    if review:
                                        quality_reports.append({
                                            "file": str(file_path.relative_to(self.repo_path)),
                                            "review": review
                                        })
                        except:
                            pass
        except:
            pass
        
        return quality_reports
    
    def display_insights(self, insights: Dict[str, Any]):
        """Display code insights in formatted output."""
        console.print(Panel(
            "[bold cyan]Code Insights & Quality Analysis[/bold cyan]",
            border_style="cyan"
        ))
        
        if insights["language_stats"]:
            lang_table = Table(title="Language Distribution")
            lang_table.add_column("Language", style="cyan")
            lang_table.add_column("Files", style="green")
            lang_table.add_column("Lines", style="yellow")
            
            for lang, stats in sorted(insights["language_stats"].items(), key=lambda x: x[1]["lines"], reverse=True):
                lang_table.add_row(lang, str(stats["files"]), str(stats["lines"]))
            
            console.print(lang_table)
        
        file_stats = insights["file_stats"]
        console.print(Panel(
            f"[bold yellow]File Statistics[/bold yellow]\n\n" +
            f"Total Files: {file_stats['total_files']}\n" +
            f"Total Lines: {file_stats['total_lines']}\n" +
            f"Avg Lines/File: {file_stats['average_lines_per_file']}",
            border_style="yellow"
        ))
        
        if insights["hotspots"]:
            console.print("\n[bold cyan]Code Hotspots (Most Changed Files):[/bold cyan]")
            for hotspot in insights["hotspots"]:
                console.print(f"  [red]{hotspot['file']}[/red] - {hotspot['changes']} changes")
        
        if insights.get("code_quality"):
            console.print("\n[bold green]AI Code Quality Reviews:[/bold green]")
            for report in insights["code_quality"]:
                console.print(f"\n[cyan]{report['file']}[/cyan]")
                review = report['review']
                console.print(f"  Quality Score: {review.get('quality_score', 'N/A')}/10")
                if review.get('issues'):
                    console.print(f"  Issues: {', '.join(review['issues'][:3])}")
                if review.get('suggestions'):
                    console.print(f"  Suggestions: {', '.join(review['suggestions'][:2])}")
