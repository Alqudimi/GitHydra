#!/usr/bin/env python3
"""
GitHydra - A comprehensive Git automation tool with beautiful terminal UI
"""

import click
import sys
from githydra.src.ui.console import console
from githydra.src.commands import (init, status, branch, commit, remote, log, stage, 
                          config, alias, sync, interactive, repair, stash, 
                          tag, reset, diff, submodule, worktree, reflog, bisect,
                          blame, archive, clean, notes, patch, statistics,
                          conflicts, rebase, bundle, compare, cloud, project, team, template,
                          analytics, ai_tools, web)
from githydra.src.logger import setup_logging

@click.group(invoke_without_command=True)
@click.version_option(version='3.0.0', prog_name='GitHydra')
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

cli.add_command(template.template_cmd)
cli.add_command(submodule.submodule_cmd)
cli.add_command(worktree.worktree_cmd)
cli.add_command(reflog.reflog_cmd)
cli.add_command(bisect.bisect_cmd)
cli.add_command(blame.blame_cmd)
cli.add_command(archive.archive_cmd)
cli.add_command(clean.clean_cmd)
cli.add_command(notes.notes_cmd)
cli.add_command(patch.patch_cmd)
cli.add_command(statistics.stats_cmd)
cli.add_command(conflicts.conflicts_cmd)
cli.add_command(rebase.rebase_cmd)
cli.add_command(bundle.bundle_cmd)
cli.add_command(compare.compare_cmd)
cli.add_command(cloud.cloud_cmd)
cli.add_command(project.project_cmd)
cli.add_command(team.team_cmd)
cli.add_command(analytics.analytics)
cli.add_command(ai_tools.ai)
cli.add_command(web.web_cmd)

if __name__ == '__main__':
    cli()