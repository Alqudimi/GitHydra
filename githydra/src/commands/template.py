"""Template management commands for GitHydra"""

import click
import json
import os
import shutil
from pathlib import Path
from tqdm import tqdm
import questionary
from githydra.src.ui.console import (
    console, print_success, print_error, print_info, print_warning,
    create_panel, create_table, create_professional_table,
    show_loading_animation, print_animated_notification, ICONS
)
from githydra.src.utils.git_helper import get_repo
from githydra.src.logger import log_command

TEMPLATES_FILE = Path(__file__).parent.parent.parent /  "templates.json"

def load_templates():
    """Load templates from JSON file"""
    TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if TEMPLATES_FILE.exists():
        try:
            with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print_error(f"Failed to load templates: {e}")
            return {}
    return {}

def save_templates(templates):
    """Save templates to JSON file"""
    try:
        TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print_error(f"Failed to save templates: {e}")
        return False

def draw_directory_structure(root_dir, prefix=""):
    """Draw directory structure as tree"""
    result = ""
    try:
        items = sorted(os.listdir(root_dir))
        for index, item in enumerate(items):
            path = os.path.join(root_dir, item)
            if os.path.isdir(path):
                connector = "└── " if index == len(items) - 1 else "├── "
                result += f"{prefix}{connector}{item}/\n"
                extension = "    " if index == len(items) - 1 else "│   "
                result += draw_directory_structure(path, prefix + extension)
            else:
                connector = "└── " if index == len(items) - 1 else "├── "
                result += f"{prefix}{connector}{item}\n"
    except Exception:
        pass
    return result

def extract_directory_contents(root_dir):
    """Extract directory structure and file contents"""
    directory_data = {
        "structure": "",
        "files": {}
    }
    
    try:
        directory_data["structure"] = draw_directory_structure(root_dir)
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    relative_path = os.path.relpath(file_path, root_dir)
                    directory_data["files"][relative_path] = content
                except Exception as e:
                    directory_data["files"][relative_path] = f"Error reading file: {str(e)}"
    except Exception as e:
        print_error(f"Failed to extract directory: {e}")
    
    return directory_data

@click.group('template')
def template_cmd():
    """Template management for project structures"""
    pass

@template_cmd.command('list')
def list_templates():
    """List all available templates"""
    templates = load_templates()
    
    if not templates:
        print_info("No templates available")
        return
    
    table_data = []
    for category, category_templates in templates.items():
        for template_name, template_data in category_templates.items():
            files_count = len(template_data.get('files', {}))
            table_data.append((
                category,
                template_name,
                str(files_count),
                "Yes" if template_data.get('structure') else "No"
            ))
    
    table = create_professional_table(
        f"{ICONS['file']} Available Templates",
        [
            ("Category", "bold cyan", "left"),
            ("Template", "yellow", "left"),
            ("Files", "green", "center"),
            ("Structure", "blue", "center")
        ],
        table_data,
        show_lines=True
    )
    
    console.print(table)
    log_command('template list', True)

@template_cmd.command('add')
@click.option('--path', '-p', help='Path to template directory')
@click.option('--category', '-c', help='Template category')
@click.option('--name', '-n', help='Template name')
def add_template(path, category, name):
    """Add a new template from directory"""
    try:
        if not path:
            path = questionary.text(
                f"{ICONS['arrow']} Enter template directory path:",
                validate=lambda x: os.path.isdir(x) or "Directory does not exist"
            ).ask()
            
            if not path:
                return
        
        if not os.path.isdir(path):
            print_error("Invalid directory path")
            return
        
        templates = load_templates()
        
        if not category:
            categories = list(templates.keys())
            if categories:
                categories.append("New category")
                category = questionary.select(
                    f"{ICONS['arrow']} Select category:",
                    choices=categories
                ).ask()
            
            if not category or category == "New category":
                category = questionary.text(
                    f"{ICONS['arrow']} Enter new category name:"
                ).ask()
        
        if not name:
            name = questionary.text(
                f"{ICONS['arrow']} Enter template name:",
                default=os.path.basename(os.path.normpath(path))
            ).ask()
        
        if not category or not name:
            print_error("Category and name are required")
            return
        
        # Check if template already exists
        if category in templates and name in templates[category]:
            overwrite = questionary.confirm(
                f"Template '{category}/{name}' already exists. Overwrite?",
                default=False
            ).ask()
            
            if not overwrite:
                print_info("Template addition cancelled")
                return
        
        show_loading_animation("Extracting template structure", 2.0)
        
        template_content = extract_directory_contents(path)
        
        if category not in templates:
            templates[category] = {}
        
        templates[category][name] = template_content
        
        if save_templates(templates):
            print_success(f"Template '{category}/{name}' added successfully")
            log_command('template add', True, f"Added {category}/{name}")
        else:
            print_error("Failed to save template")
            log_command('template add', False, "Save failed")
        
    except Exception as e:
        print_error(f"Failed to add template: {str(e)}")
        log_command('template add', False, str(e))

@template_cmd.command('remove')
@click.option('--category', '-c', help='Template category')
@click.option('--name', '-n', help='Template name')
def remove_template(category, name):
    """Remove a template"""
    try:
        templates = load_templates()
        
        if not templates:
            print_info("No templates available")
            return
        
        if not category:
            categories = list(templates.keys())
            category = questionary.select(
                f"{ICONS['arrow']} Select category:",
                choices=categories
            ).ask()
        
        if not category or category not in templates:
            print_error("Invalid category")
            return
        
        if not name:
            template_names = list(templates[category].keys())
            name = questionary.select(
                f"{ICONS['arrow']} Select template:",
                choices=template_names
            ).ask()
        
        if not name or name not in templates[category]:
            print_error("Invalid template name")
            return
        
        confirm = questionary.confirm(
            f"Are you sure you want to remove '{category}/{name}'?",
            default=False
        ).ask()
        
        if not confirm:
            print_info("Template removal cancelled")
            return
        
        del templates[category][name]
        
        # Remove category if empty
        if not templates[category]:
            del templates[category]
        
        if save_templates(templates):
            print_success(f"Template '{category}/{name}' removed successfully")
            log_command('template remove', True, f"Removed {category}/{name}")
        else:
            print_error("Failed to save changes")
            log_command('template remove', False, "Save failed")
        
    except Exception as e:
        print_error(f"Failed to remove template: {str(e)}")
        log_command('template remove', False, str(e))

@template_cmd.command('create')
@click.option('--category', '-c', help='Template category')
@click.option('--name', '-n', help='Template name')
@click.option('--output', '-o', help='Output directory')
def create_from_template(category, name, output):
    """Create project from template"""
    try:
        templates = load_templates()
        
        if not templates:
            print_info("No templates available")
            return
        
        if not category:
            categories = list(templates.keys())
            category = questionary.select(
                f"{ICONS['arrow']} Select category:",
                choices=categories
            ).ask()
        
        if not category or category not in templates:
            print_error("Invalid category")
            return
        
        if not name:
            template_names = list(templates[category].keys())
            name = questionary.select(
                f"{ICONS['arrow']} Select template:",
                choices=template_names
            ).ask()
        
        if not name or name not in templates[category]:
            print_error("Invalid template name")
            return
        
        if not output:
            output = questionary.text(
                f"{ICONS['arrow']} Enter output directory:",
                default=os.path.join(os.getcwd(), name)
            ).ask()
        
        template_data = templates[category][name]
        files_content = template_data.get('files', {})
        
        if not files_content:
            print_error("Template contains no files")
            return
        
        output_path = Path(output)
        
        if output_path.exists() and any(output_path.iterdir()):
            overwrite = questionary.confirm(
                "Output directory is not empty. Continue?",
                default=False
            ).ask()
            
            if not overwrite:
                print_info("Operation cancelled")
                return
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        show_loading_animation(f"Creating project from '{category}/{name}'", 1.0)
        
        # Save directory structure
        structure_file = output_path / "DIRECTORY_STRUCTURE.txt"
        structure_file.write_text(template_data.get('structure', 'No structure available'), encoding='utf-8')
        
        # Create files
        total_files = len(files_content)
        with tqdm(total=total_files, desc="Creating files", unit="file") as pbar:
            for file_relative_path, file_content in files_content.items():
                file_full_path = output_path / file_relative_path
                file_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_full_path.write_text(file_content, encoding='utf-8')
                pbar.update(1)
        
        print_success(f"Project created successfully in: {output_path}")
        print_info(f"Total files created: {total_files}")
        log_command('template create', True, f"Created from {category}/{name}")
        
    except Exception as e:
        print_error(f"Failed to create project: {str(e)}")
        log_command('template create', False, str(e))

@template_cmd.command('export')
@click.option('--output', '-o', help='Output JSON file path')
def export_templates(output):
    """Export templates to JSON file"""
    try:
        templates = load_templates()
        
        if not templates:
            print_info("No templates to export")
            return
        
        if not output:
            output = questionary.text(
                f"{ICONS['arrow']} Enter output file path:",
                default=str(Path.cwd() / "git_hydra_templates.json")
            ).ask()
        
        output_path = Path(output)
        if not output_path.suffix:
            output_path = output_path.with_suffix('.json')
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        
        print_success(f"Templates exported to: {output_path}")
        log_command('template export', True, f"Exported to {output_path}")
        
    except Exception as e:
        print_error(f"Failed to export templates: {str(e)}")
        log_command('template export', False, str(e))

@template_cmd.command('import')
@click.option('--input', '-i', help='Input JSON file path')
def import_templates(input):
    """Import templates from JSON file"""
    try:
        if not input:
            input = questionary.text(
                f"{ICONS['arrow']} Enter input file path:",
                validate=lambda x: os.path.isfile(x) or "File does not exist"
            ).ask()
        
        if not input or not os.path.isfile(input):
            print_error("Invalid file path")
            return
        
        with open(input, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        if not isinstance(import_data, dict):
            print_error("Invalid template file format")
            return
        
        templates = load_templates()
        
        imported_count = 0
        skipped_count = 0
        
        for category, category_templates in import_data.items():
            if category not in templates:
                templates[category] = {}
            
            for template_name, template_data in category_templates.items():
                if template_name in templates[category]:
                    overwrite = questionary.confirm(
                        f"Template '{category}/{template_name}' exists. Overwrite?",
                        default=False
                    ).ask()
                    
                    if not overwrite:
                        skipped_count += 1
                        continue
                
                templates[category][template_name] = template_data
                imported_count += 1
                print_info(f"Imported: {category}/{template_name}")
        
        if save_templates(templates):
            print_success(f"Import completed: {imported_count} imported, {skipped_count} skipped")
            log_command('template import', True, f"Imported {imported_count} templates")
        else:
            print_error("Failed to save imported templates")
            log_command('template import', False, "Save failed")
        
    except Exception as e:
        print_error(f"Failed to import templates: {str(e)}")
        log_command('template import', False, str(e))