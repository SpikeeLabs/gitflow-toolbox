import click

from gitflow_toolbox.check_branch_exists import check_branch_exists
from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab


@click.command()
@click.option("--remote/--current", default=False)
@click.argument("branch", type=str)
@click.argument("ref", type=str)
@click.pass_context
def ensure_branch(ctx: click.Context, remote: bool, branch: str, ref: str):
    """Creates a branch if doesn't exist

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
        branch (str): branch name
        ref (str): branch to create branch from
    """

    branch_exists = ctx.invoke(check_branch_exists, remote=remote, branch=branch)
    if branch_exists:
        click.echo("Branch already exists, nothing to do.")
        return

    click.echo("Branch does not exist, creating...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    project.branches.create({"branch": branch, "ref": ref})
    click.echo(f"✨ Successfully created branch {branch} from {ref}")
