import click
from rich.console import Console
from rich.panel import Panel
import git
from githydra.src.ai_service import ai_service

console = Console()


@click.group()
def ai():
    """AI-powered tools for code review and commit messages."""
    pass


@ai.command()
@click.option('--repo', '-r', default='.', help='Repository path')
def generate_commit():
    """Generate AI-powered commit message from staged changes."""
    if not ai_service.is_enabled():
        console.print("[yellow]AI service is disabled. Set GEMINI_API_KEY to enable.[/yellow]")
        return
    
    try:
        repo = git.Repo('.')
        
        if not repo.index.diff("HEAD"):
            console.print("[yellow]No staged changes found.[/yellow]")
            return
        
        diff = repo.git.diff("HEAD", "--staged")
        files = [item.a_path for item in repo.index.diff("HEAD")]
        
        console.print("[cyan]Generating commit message...[/cyan]")
        message = ai_service.generate_commit_message(diff, files)
        
        if message:
            console.print(Panel(
                f"[bold green]Suggested Commit Message:[/bold green]\n\n{message}",
                border_style="green"
            ))
            
            if click.confirm("Use this commit message?"):
                repo.index.commit(message)
                console.print("[green]✓ Committed successfully![/green]")
        else:
            console.print("[red]Failed to generate commit message[/red]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@ai.command()
@click.argument('file_path')
def review(file_path):
    """Review code file and suggest improvements."""
    if not ai_service.is_enabled():
        console.print("[yellow]AI service is disabled. Set GEMINI_API_KEY to enable.[/yellow]")
        return
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        console.print(f"[cyan]Reviewing {file_path}...[/cyan]")
        review = ai_service.review_code(code, file_path)
        
        if review:
            console.print(Panel(
                f"[bold green]Code Review Results[/bold green]\n\n" +
                f"Quality Score: {review.get('quality_score', 'N/A')}/10\n\n" +
                f"Issues:\n" + '\n'.join(f"  - {issue}" for issue in review.get('issues', [])[:5]) + "\n\n" +
                f"Suggestions:\n" + '\n'.join(f"  - {sug}" for sug in review.get('suggestions', [])[:5]),
                border_style="green"
            ))
            
            if review.get('security_concerns'):
                console.print(Panel(
                    "[bold red]Security Concerns:[/bold red]\n" +
                    '\n'.join(f"  - {concern}" for concern in review['security_concerns']),
                    border_style="red"
                ))
        else:
            console.print("[red]Failed to review code[/red]")
    
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@ai.command()
@click.argument('file_path')
@click.option('--language', '-l', default='python', help='Programming language')
def detect_bugs(file_path, language):
    """Detect potential bugs in code file."""
    if not ai_service.is_enabled():
        console.print("[yellow]AI service is disabled. Set GEMINI_API_KEY to enable.[/yellow]")
        return
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        console.print(f"[cyan]Detecting bugs in {file_path}...[/cyan]")
        bugs = ai_service.detect_bugs(code, language)
        
        if bugs and len(bugs) > 0:
            console.print(Panel(
                "[bold red]Potential Bugs Detected:[/bold red]\n\n" +
                '\n'.join(f"  - {bug}" for bug in bugs[:10]),
                border_style="red"
            ))
        elif bugs is not None:
            console.print("[green]No bugs detected![/green]")
        else:
            console.print("[red]Failed to detect bugs[/red]")
    
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@ai.command()
def status():
    """Check AI service status."""
    if ai_service.is_enabled():
        console.print("[green]✓ AI Service is ENABLED[/green]")
        console.print("  Using Gemini API for enhanced features")
    else:
        console.print("[yellow]○ AI Service is DISABLED[/yellow]")
        console.print("  Set GEMINI_API_KEY environment variable to enable")
        console.print("  All features work normally without AI")
