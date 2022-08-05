import os
import shutil
import uuid

import click
import git

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option("--from-gitlab", type=click.Choice(["current", "remote"], case_sensitive=False))
@click.argument("source_branch", type=str)
@click.option("--to-gitlab", type=click.Choice(["current", "remote"], case_sensitive=False))
@click.argument("target_branch", type=str)
@click.pass_context
def diff(
    ctx: click.Context,
    from_gitlab: tuple[str],
    source_branch: str,
    to_gitlab: tuple[str],
    target_branch: str,
):
    """Returns the 'git diff' between two branches

    Args:
        from_gitlab (str): source gitlab [current/remote]
        source_branch (str): source branch
        to_gitlab (str): destination gitlab [current/remote]
        target_branch (str): destination branch

    Returns:
        str: the 'git diff' between two branches, or an empty string (line return) if no diff
    """

    gitlab_from = CurrentGitlab() if from_gitlab == "current" else RemoteGitlab()
    gitlab_to = CurrentGitlab() if to_gitlab == "current" else RemoteGitlab()

    project_from_clone_dir = os.path.join("/tmp", f"gf_{uuid.uuid4()}")

    try:
        # Clone
        repo_from = git.Repo.clone_from(
            gitlab_from.project_authenticated_url, project_from_clone_dir, branch=source_branch
        )
        # Add remote
        repo_from.create_remote("target", gitlab_to.project_authenticated_url)
        # Diff
        repo_from.remotes.target.fetch(target_branch)
        diff_output = str(repo_from.git.diff(f"target/{target_branch}"))
        if diff_output and is_main_call(ctx):
            click.echo(diff_output)
        return diff_output
    finally:
        # Clean
        if os.path.isdir(project_from_clone_dir):
            shutil.rmtree(project_from_clone_dir)
