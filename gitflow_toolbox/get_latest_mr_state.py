import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option("--remote/--current", default=False)
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.argument("labels", type=str, nargs=-1)
@click.pass_context
def get_latest_mr_state(ctx: click.Context, remote: bool, source_branch: str, target_branch: str, labels: tuple[str]):
    """Returns the state of the latest MR from/to branch

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
        source_branch (str): branch to create
        remote_target_branch (str): branch reference to create branch from
        labels (tuple[str]): filter by labels

    Returns:
        str: state of the latest MR (opened/closed/merged/locked) or 'no-mr' if nothing was found
    """
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    mrs = project.mergerequests.list(
        source_branch=source_branch, target_branch=target_branch, order_by="created_at", labels=list(labels)
    )
    if len(mrs) == 0:
        if is_main_call(ctx):
            click.echo("no-mr")
        return "no-mr"
    if is_main_call(ctx):
        click.echo(mrs[0].state)
    return mrs[0].state
