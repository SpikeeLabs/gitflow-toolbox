import click

from gitflow_toolbox.common.get_remote_project import get_remote_project


@click.command()
@click.argument("branch", type=str)
@click.argument("ref", type=str)
def create_remote_branch(branch: str, ref: str):
    """Create Remote Branch

    Args:
        branch (str): branch to create
        ref (str): branch reference to create branch from
    """
    get_remote_project().branches.create({"branch": branch, "ref": ref})
