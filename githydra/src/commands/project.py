"""Project Management Commands - Issues, Milestones, Boards"""

import click
import questionary
import json
from pathlib import Path
from datetime import datetime
from githydra.src.ui.console import (
    console, print_success, print_error, print_warning, print_info,
    create_professional_table, create_panel, ICONS, print_section_header,
    create_colorful_list, print_animated_notification
)
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

PROJECT_DIR = Path.home() / '.githydra' / 'projects'

def ensure_project_dir():
    """Ensure project directory exists"""
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

def get_project_file(repo_path: Path) -> Path:
    """Get project file path for current repository"""
    repo_name = repo_path.name
    return PROJECT_DIR / f"{repo_name}.json"

def load_project_data(project_file: Path) -> dict:
    """Load project data from file"""
    if not project_file.exists():
        return {
            'issues': [],
            'milestones': [],
            'sprints': [],
            'labels': ['bug', 'feature', 'enhancement', 'documentation']
        }
    
    try:
        with open(project_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {
            'issues': [],
            'milestones': [],
            'sprints': [],
            'labels': []
        }

def save_project_data(project_file: Path, data: dict):
    """Save project data to file"""
    with open(project_file, 'w') as f:
        json.dump(data, f, indent=2)

@click.group('project')
def project_cmd():
    """Project management commands"""
    pass

@project_cmd.command('init')
@click.option('--name', '-n', help='Project name')
def init_project(name):
    """Initialize project management for repository"""
    try:
        repo = get_repo()
        if not repo:
            return
        
        ensure_project_dir()
        
        if not name:
            name = questionary.text(
                f"{ICONS['arrow']} Project name:",
                default=Path.cwd().name
            ).ask()
        
        project_file = get_project_file(Path.cwd())
        
        data = {
            'name': name,
            'created': datetime.now().isoformat(),
            'issues': [],
            'milestones': [],
            'sprints': [],
            'labels': ['bug', 'feature', 'enhancement', 'documentation', 'urgent', 'low-priority']
        }
        
        save_project_data(project_file, data)
        
        print_section_header("Project Initialized", ICONS['sparkles'])
        
        info = {
            'Project Name': name,
            'Location': str(Path.cwd()),
            'Config File': str(project_file),
            'Default Labels': ', '.join(data['labels'])
        }
        
        console.print(create_panel(
            "\n".join([f"[bold cyan]{k}:[/bold cyan] [white]{v}[/white]" for k, v in info.items()]),
            f"{ICONS['success']} Project Created",
            "green"
        ))
        
        log_command('project init', True, f"Name: {name}")
        
    except Exception as e:
        print_error(f"Failed to initialize project: {str(e)}")
        log_command('project init', False, str(e))

@project_cmd.command('issue-create')
@click.option('--title', '-t', help='Issue title')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high', 'urgent']), default='medium')
def create_issue(title, priority):
    """Create a new project issue"""
    try:
        ensure_project_dir()
        project_file = get_project_file(Path.cwd())
        
        if not project_file.exists():
            print_error("Project not initialized. Run 'githydra project init' first")
            return
        
        data = load_project_data(project_file)
        
        if not title:
            title = questionary.text(
                f"{ICONS['arrow']} Issue title:",
                validate=lambda x: len(x) > 0 or "Title cannot be empty"
            ).ask()
            
            if not title:
                return
        
        description = questionary.text(
            f"{ICONS['arrow']} Issue description (optional):",
            default=""
        ).ask()
        
        labels = questionary.checkbox(
            f"{ICONS['arrow']} Select labels:",
            choices=data.get('labels', [])
        ).ask()
        
        issue_id = len(data['issues']) + 1
        
        issue = {
            'id': issue_id,
            'title': title,
            'description': description,
            'priority': priority,
            'labels': labels or [],
            'status': 'open',
            'created': datetime.now().isoformat(),
            'assignee': None,
            'comments': []
        }
        
        data['issues'].append(issue)
        save_project_data(project_file, data)
        
        print_animated_notification("Issue created successfully", "success", 1.0)
        
        info = {
            'Issue ID': f"#{issue_id}",
            'Title': title,
            'Priority': priority.upper(),
            'Labels': ', '.join(labels) if labels else 'None',
            'Status': 'OPEN'
        }
        
        console.print(create_panel(
            "\n".join([f"[bold cyan]{k}:[/bold cyan] [white]{v}[/white]" for k, v in info.items()]),
            f"{ICONS['success']} Issue Created",
            "green"
        ))
        
        log_command('project issue-create', True, f"Issue #{issue_id}")
        
    except Exception as e:
        print_error(f"Failed to create issue: {str(e)}")
        log_command('project issue-create', False, str(e))

@project_cmd.command('issues')
@click.option('--status', '-s', type=click.Choice(['open', 'closed', 'all']), default='open')
def list_issues(status):
    """List project issues"""
    try:
        project_file = get_project_file(Path.cwd())
        
        if not project_file.exists():
            print_error("Project not initialized. Run 'githydra project init' first")
            return
        
        data = load_project_data(project_file)
        issues = data.get('issues', [])
        
        if status != 'all':
            issues = [i for i in issues if i['status'] == status]
        
        if not issues:
            print_info(f"No {status} issues found")
            return
        
        issues_data = []
        for issue in issues:
            priority_icon = {
                'urgent': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue['priority'], '⚪')
            
            issues_data.append((
                f"#{issue['id']}",
                issue['title'][:40] + ('...' if len(issue['title']) > 40 else ''),
                f"{priority_icon} {issue['priority'].upper()}",
                issue['status'].upper(),
                ', '.join(issue['labels'][:2]) if issue['labels'] else 'None'
            ))
        
        table = create_professional_table(
            f"{ICONS['file']} Project Issues",
            [
                ("ID", "bold yellow", "center"),
                ("Title", "cyan", "left"),
                ("Priority", "magenta", "center"),
                ("Status", "green", "center"),
                ("Labels", "blue", "left")
            ],
            issues_data,
            show_lines=True,
            caption=f"Total: {len(issues)} {status} issue(s)"
        )
        
        console.print(table)
        log_command('project issues', True)
        
    except Exception as e:
        print_error(f"Failed to list issues: {str(e)}")
        log_command('project issues', False, str(e))

@project_cmd.command('milestone-create')
@click.option('--title', '-t', help='Milestone title')
@click.option('--due-date', '-d', help='Due date (YYYY-MM-DD)')
def create_milestone(title, due_date):
    """Create a project milestone"""
    try:
        project_file = get_project_file(Path.cwd())
        
        if not project_file.exists():
            print_error("Project not initialized. Run 'githydra project init' first")
            return
        
        data = load_project_data(project_file)
        
        if not title:
            title = questionary.text(
                f"{ICONS['arrow']} Milestone title:",
                validate=lambda x: len(x) > 0 or "Title cannot be empty"
            ).ask()
        
        if not due_date:
            due_date = questionary.text(
                f"{ICONS['arrow']} Due date (YYYY-MM-DD):",
                default=datetime.now().strftime('%Y-%m-%d')
            ).ask()
        
        description = questionary.text(
            f"{ICONS['arrow']} Description (optional):",
            default=""
        ).ask()
        
        milestone_id = len(data['milestones']) + 1
        
        milestone = {
            'id': milestone_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'created': datetime.now().isoformat(),
            'status': 'active',
            'issues': []
        }
        
        data['milestones'].append(milestone)
        save_project_data(project_file, data)
        
        print_success(f"Milestone '{title}' created successfully")
        log_command('project milestone-create', True, f"Milestone #{milestone_id}")
        
    except Exception as e:
        print_error(f"Failed to create milestone: {str(e)}")
        log_command('project milestone-create', False, str(e))

@project_cmd.command('milestones')
def list_milestones():
    """List project milestones"""
    try:
        project_file = get_project_file(Path.cwd())
        
        if not project_file.exists():
            print_error("Project not initialized. Run 'githydra project init' first")
            return
        
        data = load_project_data(project_file)
        milestones = data.get('milestones', [])
        
        if not milestones:
            print_info("No milestones found")
            return
        
        milestones_data = []
        for milestone in milestones:
            milestones_data.append((
                f"#{milestone['id']}",
                milestone['title'],
                milestone['status'].upper(),
                milestone['due_date'],
                str(len(milestone.get('issues', [])))
            ))
        
        table = create_professional_table(
            f"{ICONS['star']} Project Milestones",
            [
                ("ID", "bold yellow", "center"),
                ("Title", "cyan", "left"),
                ("Status", "green", "center"),
                ("Due Date", "magenta", "center"),
                ("Issues", "blue", "center")
            ],
            milestones_data,
            show_lines=True
        )
        
        console.print(table)
        log_command('project milestones', True)
        
    except Exception as e:
        print_error(f"Failed to list milestones: {str(e)}")
        log_command('project milestones', False, str(e))

@project_cmd.command('board')
def show_board():
    """Display project board with task status"""
    try:
        project_file = get_project_file(Path.cwd())
        
        if not project_file.exists():
            print_error("Project not initialized. Run 'githydra project init' first")
            return
        
        data = load_project_data(project_file)
        issues = data.get('issues', [])
        
        print_section_header("Project Board", ICONS['chart'])
        
        open_issues = [i for i in issues if i['status'] == 'open']
        closed_issues = [i for i in issues if i['status'] == 'closed']
        
        board_data = [
            ('TODO', str(len([i for i in open_issues if i['priority'] in ['low', 'medium']])), 'cyan'),
            ('IN PROGRESS', '0', 'yellow'),
            ('URGENT', str(len([i for i in open_issues if i['priority'] == 'urgent'])), 'red'),
            ('COMPLETED', str(len(closed_issues)), 'green')
        ]
        
        table = create_professional_table(
            f"{ICONS['chart']} Task Status Overview",
            [
                ("Column", "bold cyan", "center"),
                ("Tasks", "bold yellow", "center")
            ],
            [(status, count) for status, count, _ in board_data],
            show_lines=True
        )
        
        console.print(table)
        log_command('project board', True)
        
    except Exception as e:
        print_error(f"Failed to show project board: {str(e)}")
        log_command('project board', False, str(e))
