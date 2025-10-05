"""Configuration management"""

import click
from pathlib import Path
import yaml
from src.ui.console import console, print_success, print_error, create_table
from src.utils.git_helper import get_repo
from src.logger import log_command

CONFIG_DIR = Path.home() / ".githydra"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

def load_config():
    """Load GitHydra configuration"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_config(config):
    """Save GitHydra configuration"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

@click.group('config')
def config_cmd():
    """Configuration management"""
    pass

@config_cmd.command('list')
@click.option('--global', 'is_global', is_flag=True, help='Show global Git config')
def list_config(is_global):
    """List configuration"""
    if is_global:
        repo = get_repo()
        if repo:
            try:
                config = repo.config_reader()
                table = create_table("Git Configuration", ["Key", "Value"])
                
                for section in config.sections():
                    for key, value in config.items(section):
                        table.add_row(f"{section}.{key}", value)
                
                console.print(table)
                log_command('config list', True)
            except Exception as e:
                print_error(f"Failed to read Git config: {str(e)}")
        else:
            print_error("Not in a Git repository")
    else:
        config = load_config()
        
        if not config:
            print_error("No GitHydra configuration found")
            return
        
        table = create_table("GitHydra Configuration", ["Key", "Value"])
        
        for key, value in config.items():
            table.add_row(key, str(value))
        
        console.print(table)
        log_command('config list', True)

@config_cmd.command('set')
@click.argument('key')
@click.argument('value')
@click.option('--global', 'is_global', is_flag=True, help='Set global Git config')
def set_config(key, value, is_global):
    """Set configuration value"""
    if is_global:
        repo = get_repo()
        if repo:
            try:
                with repo.config_writer() as config:
                    section, option = key.rsplit('.', 1)
                    config.set_value(section, option, value)
                print_success(f"Set {key} = {value}")
                log_command('config set', True, f"Set {key}")
            except Exception as e:
                print_error(f"Failed to set Git config: {str(e)}")
        else:
            print_error("Not in a Git repository")
    else:
        config = load_config()
        config[key] = value
        save_config(config)
        print_success(f"Set {key} = {value}")
        log_command('config set', True, f"Set {key}")

@config_cmd.command('get')
@click.argument('key')
def get_config(key):
    """Get configuration value"""
    config = load_config()
    
    if key in config:
        console.print(f"{key} = {config[key]}")
    else:
        print_error(f"Configuration key '{key}' not found")

@config_cmd.command('unset')
@click.argument('key')
def unset_config(key):
    """Remove configuration value"""
    config = load_config()
    
    if key in config:
        del config[key]
        save_config(config)
        print_success(f"Removed {key}")
        log_command('config unset', True, f"Removed {key}")
    else:
        print_error(f"Configuration key '{key}' not found")
