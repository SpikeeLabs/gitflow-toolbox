import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option("--remote/--current", default=False)
@click.pass_context
def get_project_http_url(ctx: click.Context, remote: bool):
    """Get Gitlab project SSH URL (for cloning)

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
    """
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    url = project.attributes.get("http_url_to_repo")
    if is_main_call(ctx):
        click.echo(url)
    return url
