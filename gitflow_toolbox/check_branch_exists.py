import sys

import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.argument("branch", type=str)
@click.option(
    "--remote/--current",
    "-r/-c",
    default=False,
    help="Flag which allow you to chose between configured target or remote to run this tool."
    " By default, the script use --current flag.",
)
@click.pass_context
def check_branch_exists(ctx: click.Context, branch: str, remote: bool = False):
    """Checks if the given BRANCH exists

    Return True if a branch exists (exit code 0), False otherwise (exit code 1)
    \f

    Args:
        branch (str): branch name
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Default to False.

    Returns:
        bool: True if branch exists (exit code 0), False otherwise (exit code 1)
    """
    click.echo(f"Checking if {branch} branch exists...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    branch_exists = next((True for b in project.branches.list() if b.name == branch), False)
    if is_main_call(ctx):
        click.echo(branch_exists)
        sys.exit(0 if branch_exists else 1)
    return branch_exists
