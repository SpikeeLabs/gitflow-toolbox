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
def get_project_ssh_url(ctx: click.Context, remote: bool = False):
    """Get Gitlab project SSH URL (for cloning)\f

    Args:
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Default to False.
    """
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    ssh_url = project.attributes.get("ssh_url_to_repo")
    if is_main_call(ctx):
        click.echo(ssh_url)
    return ssh_url
