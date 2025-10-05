#!/usr/bin/env python3
"""
GitHydra - A comprehensive Git automation tool with beautiful terminal UI
"""

import click
import sys
from src.ui.console import console
from src.commands import (init, status, branch, commit, remote, log, stage, 
                          config, alias, sync, interactive, repair, stash, 
                          tag, reset, diff)
from src.logger import setup_logging

@click.group(invoke_without_command=True)
@click.version_option(version='2.0.0', prog_name='GitHydra')
@click.pass_context
def cli(ctx):
    """
    GitHydra - Beautiful and powerful Git automation tool
    
    Manage all your Git operations with an elegant terminal interface.
    
    Use 'githydra interactive' for menu-driven interface.
    """
    ctx.ensure_object(dict)
    setup_logging()
    
    # إذا لم يتم إرسال أي أمر، تشغيل الوضع التفاعلي
    if ctx.invoked_subcommand is None:
        ctx.invoke(interactive.interactive_cmd)

cli.add_command(interactive.interactive_cmd)
cli.add_command(init.init_cmd)
cli.add_command(status.status_cmd)
cli.add_command(branch.branch_cmd)
cli.add_command(commit.commit_cmd)
cli.add_command(remote.remote_cmd)
cli.add_command(log.log_cmd)
cli.add_command(stage.stage_cmd)
cli.add_command(sync.sync_cmd)
cli.add_command(repair.repair_cmd)
cli.add_command(stash.stash_cmd)
cli.add_command(tag.tag_cmd)
cli.add_command(reset.reset_cmd)
cli.add_command(reset.revert_cmd)
cli.add_command(reset.cherry_pick_cmd)
cli.add_command(diff.diff_cmd)
cli.add_command(config.config_cmd)
cli.add_command(alias.alias_cmd)

if __name__ == '__main__':
    cli()