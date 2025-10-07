import click
from rich.console import Console
from githydra.src.analytics import WeeklyReport, TeamAnalytics, CodeInsights

console = Console()


@click.group()
def analytics():
    """Analytics and insights commands."""
    pass


@analytics.command()
@click.option('--weeks', '-w', default=1, help='Number of weeks to analyze')
@click.option('--repo', '-r', default='.', help='Repository path')
def weekly_report(weeks, repo):
    """Generate weekly development report."""
    try:
        report_gen = WeeklyReport(repo)
        report = report_gen.generate_report(weeks=weeks)
        report_gen.display_report(report)
    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")


@analytics.command()
@click.option('--days', '-d', default=30, help='Number of days to analyze')
@click.option('--repo', '-r', default='.', help='Repository path')
def team(days, repo):
    """Analyze team collaboration and productivity."""
    try:
        team_analytics = TeamAnalytics(repo)
        analytics = team_analytics.analyze_team(days=days)
        team_analytics.display_analytics(analytics)
    except Exception as e:
        console.print(f"[red]Error analyzing team: {e}[/red]")


@analytics.command()
@click.option('--repo', '-r', default='.', help='Repository path')
def insights(repo):
    """Analyze code quality and complexity."""
    try:
        code_insights = CodeInsights(repo)
        insights = code_insights.analyze_repository()
        code_insights.display_insights(insights)
    except Exception as e:
        console.print(f"[red]Error analyzing code: {e}[/red]")
