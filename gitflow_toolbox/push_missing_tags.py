import os
import shutil
import sys
import uuid

import click
import git

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.get_project_http_url import get_project_http_url


@click.command()
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
@click.pass_context
def push_missing_tags(
    ctx: click.Context,
    from_gitlab: str = "remote",
    to_gitlab: str = "remote",
):
    """Push missing tags from a repository to another\f

    Args:
        from_gitlab (str, optional): source gitlab [current/remote]. Defaults to 'remote'.
        to_gitlab (str, optional): destination gitlab [current/remote]. Defaults to 'remote'.
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
        repo_from = git.Repo.clone_from(gitlab_from.project_authenticated_url, project_from_clone_dir)
        # Add remote
        project_to_http_url = ctx.invoke(get_project_http_url, remote=(to_gitlab == "remote"))
        click.echo(f"Adding remote to {project_to_http_url}")
        repo_from.create_remote("target", gitlab_to.project_authenticated_url)
        repo_from.remotes.target.fetch()

        # Get all tags in FROM git not in TO git
        source_tags: set[git.Tag] = set()
        target_tags: set[git.Tag] = set()
        for tag in repo_from.tags:
            if tag.remote_name == repo_from.remotes.target.name:
                target_tags.add(tag)
            else:
                source_tags.add(tag)

        # Push missing tags from target to source
        for item in target_tags - source_tags:
            click.echo(f"Pushing {from_gitlab} {item.name} into {to_gitlab} ...")
            changes = repo_from.remotes.target.push(item)
            for change in changes:
                click.echo(change.summary)
                if "rejected" in change.summary:
                    click.echo(f"❌ Couldn't push {item.name} to {to_gitlab}")
                    sys.exit(1)
            click.echo(f"✨ Successfully pushed {from_gitlab} tags into {to_gitlab}")

    finally:
        # Clean
        if os.path.isdir(project_from_clone_dir):
            click.echo(f"Removing cache {project_from_clone_dir}")
            shutil.rmtree(project_from_clone_dir)
