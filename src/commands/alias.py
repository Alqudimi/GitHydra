"""Alias management for common workflows"""

import click
from pathlib import Path
import yaml
from src.ui.console import console, print_success, print_error, create_table
from src.logger import log_command

ALIAS_DIR = Path.home() / ".githydra"
ALIAS_FILE = ALIAS_DIR / "aliases.yaml"

DEFAULT_ALIASES = {
    'st': 'status',
    'co': 'branch switch',
    'br': 'branch list',
    'ci': 'commit',
    'unstage': 'stage remove',
    'last': 'log -n 1',
    'visual': 'log --graph',
}

def load_aliases():
    """Load aliases from file"""
    ALIAS_DIR.mkdir(parents=True, exist_ok=True)
    
    if ALIAS_FILE.exists():
        with open(ALIAS_FILE, 'r') as f:
            return yaml.safe_load(f) or DEFAULT_ALIASES
    else:
        save_aliases(DEFAULT_ALIASES)
        return DEFAULT_ALIASES

def save_aliases(aliases):
    """Save aliases to file"""
    ALIAS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(ALIAS_FILE, 'w') as f:
        yaml.dump(aliases, f, default_flow_style=False)

@click.group('alias')
def alias_cmd():
    """Manage command aliases"""
    pass

@alias_cmd.command('list')
def list_aliases():
    """List all aliases"""
    aliases = load_aliases()
    
    if not aliases:
        print_error("No aliases configured")
        return
    
    table = create_table("Command Aliases", ["Alias", "Command"])
    
    for alias, command in sorted(aliases.items()):
        table.add_row(f"[cyan]{alias}[/cyan]", command)
    
    console.print(table)
    log_command('alias list', True)

@alias_cmd.command('add')
@click.argument('alias')
@click.argument('command')
def add_alias(alias, command):
    """Add a new alias"""
    aliases = load_aliases()
    
    if alias in aliases:
        print_error(f"Alias '{alias}' already exists. Use 'remove' first.")
        return
    
    aliases[alias] = command
    save_aliases(aliases)
    print_success(f"Added alias: {alias} -> {command}")
    log_command('alias add', True, f"Alias '{alias}' added")

@alias_cmd.command('remove')
@click.argument('alias')
def remove_alias(alias):
    """Remove an alias"""
    aliases = load_aliases()
    
    if alias not in aliases:
        print_error(f"Alias '{alias}' not found")
        return
    
    del aliases[alias]
    save_aliases(aliases)
    print_success(f"Removed alias: {alias}")
    log_command('alias remove', True, f"Alias '{alias}' removed")

@alias_cmd.command('clear')
def clear_aliases():
    """Clear all aliases"""
    save_aliases({})
    print_success("All aliases cleared")
    log_command('alias clear', True)
