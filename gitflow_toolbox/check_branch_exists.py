import sys

import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option("--remote/--current", default=False)
@click.argument("branch", type=str)
@click.pass_context
def check_branch_exists(ctx: click.Context, remote: bool, branch: str):
    """Checks if a branch exists

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
        branch (str): branch name
    """
    click.echo(f"Checking if {branch} branch exists...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    branch_exists = next((True for b in project.branches.list() if b.name == branch), False)
    if is_main_call(ctx):
        click.echo(branch_exists)
        sys.exit(0 if branch_exists else 1)
    return branch_exists
