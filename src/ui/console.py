"""Console and UI utilities using Rich library"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.text import Text
from rich import box

console = Console()

def print_success(message: str):
    """Print success message in green"""
    console.print(f"✓ {message}", style="bold green")

def print_error(message: str):
    """Print error message in red"""
    console.print(f"✗ {message}", style="bold red")

def print_warning(message: str):
    """Print warning message in yellow"""
    console.print(f"⚠ {message}", style="bold yellow")

def print_info(message: str):
    """Print info message in blue"""
    console.print(f"ℹ {message}", style="bold cyan")

def create_panel(content, title: str, border_style: str = "cyan"):
    """Create a beautiful panel"""
    return Panel(content, title=title, border_style=border_style, box=box.ROUNDED)

def create_table(title: str, columns: list, rows: list = []):
    """Create a formatted table"""
    table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold cyan")
    
    for col in columns:
        table.add_column(col, style="white")
    
    if rows:
        for row in rows:
            table.add_row(*row)
    
    return table

def create_tree(label: str, guide_style: str = "cyan"):
    """Create a tree structure for branches"""
    return Tree(label, guide_style=guide_style)

def print_diff(diff_text: str):
    """Print colorized diff"""
    syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
    console.print(syntax)

def create_progress():
    """Create a progress bar"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    )
