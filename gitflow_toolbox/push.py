import os
import shutil
import sys
import uuid

import click
import git

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.get_project_http_url import get_project_http_url


@click.command()
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.option(
    "--from-gitlab",
    "-f",
    type=click.Choice(["current", "remote"], case_sensitive=False),
    help="Flag which allow you to chose between the current gitlab or the remote gitlab for the FROM role."
    " Defaults to 'remote'.",
)
@click.option(
    "--to-gitlab",
    "-t",
    type=click.Choice(["current", "remote"], case_sensitive=False),
    help="Flag which allow you to chose between the current gitlab or the remote gitlab for the TO role."
    " Defaults to 'remote'.",
)
@click.option("--force", "-f", is_flag=True, type=bool, help="Flag to enable force push")
@click.pass_context
def push(
    ctx: click.Context,
    source_branch: str,
    target_branch: str,
    from_gitlab: str = "remote",
    to_gitlab: str = "remote",
    force: bool = False,
):
    """Push commits from SOURCE_BRANCH to TARGET_BRANCH\f

    Args:
        source_branch (str): source branch
        target_branch (str): destination branch
        from_gitlab (str, optional): source gitlab [current/remote]. Defaults to 'remote'.
        to_gitlab (str, optional): destination gitlab [current/remote]. Defaults to 'remote'.
        force (bool, optional): whether to force push. Defaults to False.
    """
    to_gitlab = to_gitlab.lower()
    from_gitlab = from_gitlab.lower()

    gitlab_from = CurrentGitlab() if from_gitlab == "current" else RemoteGitlab()
    gitlab_to = CurrentGitlab() if to_gitlab == "current" else RemoteGitlab()

    project_from_http_url = ctx.invoke(get_project_http_url, remote=(from_gitlab == "remote"))
    project_from_clone_dir = os.path.join("/tmp", f"gf_{uuid.uuid4()}")

    click.echo(f"Cloning {project_from_http_url} into {project_from_clone_dir}")
    try:
        # Clone
        repo_from = git.Repo.clone_from(
            gitlab_from.project_authenticated_url, project_from_clone_dir, branch=source_branch
        )
        # Add remote
        project_to_http_url = ctx.invoke(get_project_http_url, remote=(to_gitlab == "remote"))
        click.echo(f"Adding remote to {project_to_http_url}")
        repo_from.create_remote("target", gitlab_to.project_authenticated_url)
        # Push
        repo_from.remotes.target.fetch(target_branch)
        click.echo(f"Pushing {from_gitlab} {source_branch} into {to_gitlab} {target_branch} (force={force})")
        changes = repo_from.remotes.target.push(refspec=f"{source_branch}:{target_branch}", force=force)
        for change in changes:
            click.echo(change.summary)
            if "rejected" in change.summary:
                click.echo(f"❌ Couldn't push changes to {to_gitlab} {target_branch}")
                sys.exit(1)
        click.echo(f"✨ Successfully pushed {from_gitlab} {source_branch} into {to_gitlab} {target_branch}")

    finally:
        # Clean
        if os.path.isdir(project_from_clone_dir):
            click.echo(f"Removing cache {project_from_clone_dir}")
            shutil.rmtree(project_from_clone_dir)
