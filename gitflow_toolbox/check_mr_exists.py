import sys

import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option("--remote/--current", default=False)
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.option("--state", type=str, default="opened")
@click.pass_context
def check_mr_exists(ctx: click.Context, remote: bool, source_branch: str, target_branch: str, state: str):
    """Check if a MR exists

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
        source_branch (str): branch to create
        remote_target_branch (str): branch reference to create branch from

    Returns:
        bool: True if a MR exists (exit code 0), False otherwise (exit code 1)
    """
    click.echo(f"Checking if an opened merge request from {source_branch} to {target_branch} exists...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    mrs = project.mergerequests.list(state=state, source_branch=source_branch, target_branch=target_branch)
    mr_exists = len(mrs) != 0
    if is_main_call(ctx):
        click.echo(mr_exists)
        sys.exit(0 if mr_exists else 1)
    return mr_exists
