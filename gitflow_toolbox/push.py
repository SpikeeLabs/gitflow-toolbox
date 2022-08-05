import os
import shutil
import sys
import uuid

import click
import git

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.get_project_http_url import get_project_http_url


@click.command()
@click.option("--from-gitlab", type=click.Choice(["current", "remote"], case_sensitive=False))
@click.argument("source_branch", type=str)
@click.option("--to-gitlab", type=click.Choice(["current", "remote"], case_sensitive=False))
@click.argument("target_branch", type=str)
@click.option("--force", is_flag=True, type=bool)
@click.pass_context
def push(
    ctx: click.Context,
    from_gitlab: tuple[str],
    source_branch: str,
    to_gitlab: tuple[str],
    target_branch: str,
    force: bool,
):
    """Push commits from a branch to another branch

    Args:
        from_gitlab (str): source gitlab [current/remote]
        source_branch (str): source branch
        to_gitlab (str): destination gitlab [current/remote]
        target_branch (str): destination branch
        force (bool): whether to force push (default: False)
    """

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
