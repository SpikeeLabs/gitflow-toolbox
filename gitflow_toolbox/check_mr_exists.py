import sys

import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.option(
    "--remote/--current",
    "-r/-c",
    default=False,
    help="Flag which allow you to chose between configured target or remote to run this tool."
    " By default, the script use --current flag.",
)
@click.option(
    "--state",
    "-s",
    type=click.Choice(["opened", "closed", "locked", "merged"], case_sensitive=False),
    default="opened",
    help="Flag which allow you to filter merge request during search if it exists by the given state."
    " By default to 'opened'.",
)
@click.pass_context
def check_mr_exists(
    ctx: click.Context, source_branch: str, target_branch: str, remote: bool = False, state: str = "opened"
):
    """Check if the merge request between SOURCE_BRANCH and TARGET_BRANCH exists

    Return True if a MR exists (exit code 0), False otherwise (exit code 1)
    \f

    Args:
        source_branch (str): branch to create
        remote_target_branch (str): branch reference to create branch from
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Defaults to False.
        state (str, optional): The state of the merge request expected. Defaults to "opened".

    Returns:
        bool: True if a MR exists (exit code 0), False otherwise (exit code 1)
    """
    click.echo(f"Checking if an opened merge request from {source_branch} to {target_branch} exists...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    mrs = project.mergerequests.list(state=state.lower(), source_branch=source_branch, target_branch=target_branch)
    mr_exists = len(mrs) != 0
    if is_main_call(ctx):
        click.echo(mr_exists)
        sys.exit(0 if mr_exists else 1)
    return mr_exists
