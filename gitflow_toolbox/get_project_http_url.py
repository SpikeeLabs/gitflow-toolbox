import click

from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.common.is_main_call import is_main_call


@click.command()
@click.option(
    "--remote/--current",
    "-r/-c",
    default=False,
    help="Flag which allow you to chose between configured target or remote to run this tool."
    " By default, the script use --current flag.",
)
@click.pass_context
def get_project_http_url(ctx: click.Context, remote: bool = False):
    """Get Gitlab project SSH URL (for cloning)\f

    Args:
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Default to False.
    """
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    url = project.attributes.get("http_url_to_repo")
    if is_main_call(ctx):
        click.echo(url)
    return url
