import click

from gitflow_toolbox.check_branch_exists import check_branch_exists
from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab


@click.command()
@click.argument("branch", type=str)
@click.argument("ref", type=str)
@click.option(
    "--remote/--current",
    "-r/-c",
    default=False,
    help="Flag which allow you to chose between configured target or remote to run this tool."
    " By default, the script use --current flag.",
)
@click.pass_context
def ensure_branch(ctx: click.Context, branch: str, ref: str, remote: bool = False):
    """Creates the branch BRANCH using branch REF if the target doesn't exist\f

    Args:
        branch (str): branch name
        ref (str): branch to create branch from
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Default to False.
    """

    branch_exists = ctx.invoke(check_branch_exists, remote=remote, branch=branch)
    if branch_exists:
        click.echo("Branch already exists, nothing to do.")
        return

    click.echo("Branch does not exist, creating...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    project.branches.create({"branch": branch, "ref": ref})
    click.echo(f"✨ Successfully created branch {branch} from {ref}")
