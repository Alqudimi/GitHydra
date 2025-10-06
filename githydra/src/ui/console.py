"""Console and UI utilities using Rich library - Enhanced version with beautiful styling"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.syntax import Syntax
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich import box
from rich.live import Live
from rich.spinner import Spinner
import time
from typing import List, Optional

console = Console()

ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'git': '🔱',
    'branch': '🌿',
    'commit': '📝',
    'tag': '🏷️',
    'remote': '🌐',
    'folder': '📁',
    'file': '📄',
    'rocket': '🚀',
    'sparkles': '✨',
    'fire': '🔥',
    'star': '⭐',
    'check': '✓',
    'cross': '✗',
    'arrow': '➜',
    'diamond': '◆',
    'circle': '●',
    'square': '■',
    'plus': '➕',
    'minus': '➖',
    'wrench': '🔧',
    'magnify': '🔍',
    'shield': '🛡️',
    'clock': '🕐',
    'chart': '📊',
    'book': '📚',
    'save': '💾',
    'trash': '🗑️',
    'upload': '⬆️',
    'download': '⬇️',
    'sync': '🔄',
    'merge': '🔀',
    'package': '📦',
}

COLOR_THEMES = {
    'success': 'bold green',
    'error': 'bold red',
    'warning': 'bold yellow',
    'info': 'bold cyan',
    'primary': 'bold magenta',
    'secondary': 'bold blue',
    'accent': 'bold bright_cyan',
    'highlight': 'bold bright_yellow',
    'muted': 'dim white',
}

def print_banner():
    """Print beautiful Githydra banner with branding"""
    banner_text = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗ ██████╗   ║
║  ██╔════╝ ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗  ║
║  ██║  ███╗██║   ██║   ███████║ ╚████╔╝ ██║  ██║██████╔╝  ║
║  ██║   ██║██║   ██║   ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗  ║
║  ╚██████╔╝██║   ██║   ██║  ██║   ██║   ██████╔╝██║  ██║  ║
║   ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝  ║
║                                                           ║
║            🔱 Git Automation & Management Tool 🔱         ║
║                                                           ║
║         Developer: Abdulaziz Alqudimi                     ║
║         Version: 3.0.0                                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner_text, style="bold cyan", justify="center")

def print_success(message: str, icon: bool = True):
    """Print success message with icon and animation"""
    icon_str = f"{ICONS['success']} " if icon else ""
    console.print(f"{icon_str}{message}", style=COLOR_THEMES['success'])

def print_error(message: str, icon: bool = True):
    """Print error message with icon"""
    icon_str = f"{ICONS['error']} " if icon else ""
    console.print(f"{icon_str}{message}", style=COLOR_THEMES['error'])

def print_warning(message: str, icon: bool = True):
    """Print warning message with icon"""
    icon_str = f"{ICONS['warning']} " if icon else ""
    console.print(f"{icon_str}{message}", style=COLOR_THEMES['warning'])

def print_info(message: str, icon: bool = True):
    """Print info message with icon"""
    icon_str = f"{ICONS['info']} " if icon else ""
    console.print(f"{icon_str}{message}", style=COLOR_THEMES['info'])

def print_animated_notification(message: str, notification_type: str = "info", duration: float = 1.5):
    """Print an animated notification with spinner"""
    icon_map = {
        'success': ICONS['success'],
        'error': ICONS['error'],
        'warning': ICONS['warning'],
        'info': ICONS['info'],
    }
    
    color_map = {
        'success': 'green',
        'error': 'red',
        'warning': 'yellow',
        'info': 'cyan',
    }
    
    icon = icon_map.get(notification_type, ICONS['info'])
    color = color_map.get(notification_type, 'cyan')
    
    with console.status(f"[{color}]{icon} {message}[/{color}]", spinner="dots"):
        time.sleep(duration)

def create_panel(content, title: str, border_style: str = "cyan", subtitle: Optional[str] = None):
    """Create a beautiful panel with optional subtitle"""
    return Panel(
        content, 
        title=f"[bold]{title}[/bold]",
        subtitle=subtitle,
        border_style=border_style, 
        box=box.DOUBLE,
        padding=(1, 2)
    )

def create_professional_table(
    title: str, 
    columns: List[tuple], 
    rows: List[tuple] = [], 
    show_lines: bool = True,
    caption: Optional[str] = None
):
    """
    Create a professionally formatted table with enhanced styling
    
    Args:
        title: Table title
        columns: List of tuples (column_name, style, justify)
        rows: List of tuples containing row data
        show_lines: Whether to show lines between rows
        caption: Optional caption below the table
    """
    table = Table(
        title=f"[bold cyan]{title}[/bold cyan]",
        box=box.DOUBLE_EDGE,
        show_header=True,
        header_style="bold magenta on black",
        show_lines=show_lines,
        caption=caption,
        caption_style="dim italic",
        border_style="bright_cyan",
        row_styles=["", "dim"]
    )
    
    for col in columns:
        if len(col) == 3:
            name, style, justify = col
            table.add_column(name, style=style, justify=justify)
        else:
            table.add_column(col[0], style=col[1] if len(col) > 1 else "white")
    
    if rows:
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
    
    return table

def create_table(title: str, columns: list, rows: list = []):
    """Create a formatted table (backward compatible)"""
    column_tuples = [(col, "white", "left") for col in columns]
    return create_professional_table(title, column_tuples, rows)

def create_colorful_list(items: List[tuple], title: str = ""):
    """
    Create a beautiful colored list
    
    Args:
        items: List of tuples (icon, text, style)
        title: Optional title for the list
    """
    content = ""
    if title:
        content += f"[bold cyan]{title}[/bold cyan]\n\n"
    
    for item in items:
        if len(item) == 3:
            icon, text, style = item
            content += f"{icon} [{style}]{text}[/{style}]\n"
        else:
            icon, text = item
            content += f"{icon} {text}\n"
    
    return content

def create_tree(label: str, guide_style: str = "cyan"):
    """Create a tree structure for branches"""
    return Tree(
        f"[bold {guide_style}]{label}[/bold {guide_style}]", 
        guide_style=guide_style
    )

def print_diff(diff_text: str):
    """Print colorized diff"""
    syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
    console.print(syntax)

def create_modern_progress():
    """Create a beautiful modern progress bar with multiple columns"""
    return Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(
            bar_width=40,
            style="cyan",
            complete_style="bright_cyan",
            finished_style="bright_green"
        ),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    )

def create_progress():
    """Create a progress bar (backward compatible)"""
    return create_modern_progress()

def show_loading_animation(message: str, duration: float = 2.0):
    """Show a loading animation with message"""
    with console.status(f"[bold cyan]{ICONS['sync']} {message}...[/bold cyan]", spinner="dots"):
        time.sleep(duration)

def print_section_header(title: str, icon: str = None):
    """Print a beautiful section header"""
    icon_str = f"{icon} " if icon else f"{ICONS['diamond']} "
    header_text = f"{icon_str}{title}"
    console.print()
    console.rule(f"[bold magenta]{header_text}[/bold magenta]", style="bright_cyan")
    console.print()

def print_separator(style: str = "cyan"):
    """Print a separator line"""
    console.rule(style=style)

def create_status_badge(status: str, text: str):
    """Create a status badge with appropriate coloring"""
    status_colors = {
        'success': 'green',
        'error': 'red',
        'warning': 'yellow',
        'info': 'cyan',
        'pending': 'yellow',
        'active': 'bright_green',
    }
    
    color = status_colors.get(status.lower(), 'white')
    icon = ICONS.get(status.lower(), ICONS['circle'])
    
    return f"{icon} [{color}]{text}[/{color}]"

def print_footer():
    """Print beautiful footer with developer credit"""
    footer = Panel(
        Align.center(
            f"[dim]Made with {ICONS['fire']} by [bold cyan]Abdulaziz Alqudimi[/bold cyan]\n"
            f"Githydra v3.0 - Powerful Git Automation Tool[/dim]"
        ),
        box=box.DOUBLE,
        border_style="dim cyan"
    )
    console.print(footer)

def create_info_box(title: str, data: dict, icon: str = None):
    """Create an information box with key-value pairs"""
    icon_str = f"{icon} " if icon else f"{ICONS['info']} "
    content = ""
    
    for key, value in data.items():
        content += f"[bold cyan]{key}:[/bold cyan] [white]{value}[/white]\n"
    
    return create_panel(content.strip(), f"{icon_str}{title}", "cyan")

def print_git_status_summary(staged: int, modified: int, untracked: int):
    """Print a beautiful summary of git status"""
    table = create_professional_table(
        f"{ICONS['git']} Repository Status Summary",
        [
            ("Category", "bold cyan", "left"),
            ("Count", "bold yellow", "center"),
            ("Status", "bold", "center")
        ],
        [
            (f"{ICONS['plus']} Staged files", str(staged), create_status_badge('success' if staged > 0 else 'info', 'Ready to commit' if staged > 0 else 'None')),
            (f"{ICONS['file']} Modified files", str(modified), create_status_badge('warning' if modified > 0 else 'info', 'Uncommitted changes' if modified > 0 else 'None')),
            (f"{ICONS['folder']} Untracked files", str(untracked), create_status_badge('warning' if untracked > 0 else 'info', 'Not in git' if untracked > 0 else 'None'))
        ],
        show_lines=True
    )
    console.print(table)

def print_command_result(command: str, success: bool, message: str = ""):
    """Print command execution result with beautiful formatting"""
    if success:
        panel_content = f"{ICONS['success']} [bold green]Command executed successfully[/bold green]\n\n"
        panel_content += f"[cyan]Command:[/cyan] [white]{command}[/white]"
        if message:
            panel_content += f"\n[cyan]Result:[/cyan] [white]{message}[/white]"
        console.print(create_panel(panel_content, f"{ICONS['check']} Success", "green"))
    else:
        panel_content = f"{ICONS['error']} [bold red]Command execution failed[/bold red]\n\n"
        panel_content += f"[cyan]Command:[/cyan] [white]{command}[/white]"
        if message:
            panel_content += f"\n[cyan]Error:[/cyan] [red]{message}[/red]"
        console.print(create_panel(panel_content, f"{ICONS['cross']} Failed", "red"))
