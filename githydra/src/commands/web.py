#!/usr/bin/env python3
"""
Web Dashboard Command for GitHydra
"""

import click
import sys
import os
import webbrowser
import threading
import time

@click.command('web', help='Launch GitHydra web dashboard')
@click.option('--port', '-p', default=5000, help='Port to run the web server on')
@click.option('--no-browser', is_flag=True, help='Don\'t open browser automatically')
@click.option('--debug', is_flag=True, help='Run in debug mode')
def web_cmd(port, no_browser, debug):
    """Launch the GitHydra web dashboard"""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    try:
        # Import and run the Flask app
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'web'))
        from web.app import run_web_server
        
        console.print(Panel.fit(
            "[bold cyan]🚀 GitHydra Web Dashboard[/bold cyan]\n"
            f"[yellow]Starting server on port {port}...[/yellow]",
            border_style="cyan"
        ))
        
        # Open browser after a delay
        if not no_browser:
            def open_browser():
                time.sleep(1.5)
                webbrowser.open(f'http://localhost:{port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
        
        # Run the web server
        run_web_server(repo_path='.', port=port, debug=debug)
        
    except ImportError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        console.print("[yellow]Tip:[/yellow] Make sure Flask is installed: pip install flask", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error starting web server:[/bold red] {str(e)}", style="red")
        sys.exit(1)
