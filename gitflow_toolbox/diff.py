import os
import shutil
import uuid

import click
import git

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.option(
    "--from-gitlab",
    "-f",
    type=click.Choice(["current", "remote"], case_sensitive=False),
    help="Flag which allow you to chose between the current gitlab or the remote gitlab for the FROM role of the diff."
    " Defaults to 'remote'.",
)
@click.option(
    "--to-gitlab",
    "-t",
    type=click.Choice(["current", "remote"], case_sensitive=False),
    help="Flag which allow you to chose between the current gitlab or the remote gitlab for the TO role of the diff."
    " Defaults to 'remote'.",
)
@click.pass_context
def diff(
    ctx: click.Context,
    source_branch: str,
    target_branch: str,
    from_gitlab: str = "remote",
    to_gitlab: str = "remote",
):
    """Returns the 'git diff' between SOURCE_BRANCH and TARGET_BRANCH\f

    Args:
        source_branch (str): source branch
        target_branch (str): destination branch
        from_gitlab (str, optional): source gitlab [current/remote]. Defaults to "remote".
        to_gitlab (str, optional): destination gitlab [current/remote]. Defaults to "remote".

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
        # Clean created directory by git lib during clone_from
        if os.path.isdir(project_from_clone_dir):
            # These lines aren't tested by unit test because git doesn't impact file-system (mocked)
            shutil.rmtree(project_from_clone_dir)  # pragma: no cover
