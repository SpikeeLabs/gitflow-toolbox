import click

from gitflow_toolbox.check_mr_exists import check_mr_exists
from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab


@click.command()
@click.option("--remote/--current", default=False)
@click.option("--keep-source-branch", is_flag=True)
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.argument("title", type=str)
@click.argument("description", type=str)
@click.argument("labels", type=str, nargs=-1)
@click.pass_context
def ensure_mr(
    ctx: click.Context,
    remote: bool,
    keep_source_branch: bool,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
    labels: tuple[str],
):
    """Create a MR if not exists

    Args:
        remote (bool): whether to check on the current gitlab or remote gitlab (True=remote)
        keep_source_branch (bool): if you want to keep source branch or not
        source_branch (str): branch to create
        target_branch (str): branch reference to create branch from
        title (str): MR title
        description (str): MR description
        labels (tuple[str]): MR labels
    """

    mr_exists = ctx.invoke(check_mr_exists, remote=remote, source_branch=source_branch, target_branch=target_branch)
    if mr_exists:
        click.echo("MR already exists, nothing to do.")
        return

    click.echo("MR does not exist, creating...")
    project = RemoteGitlab().project if remote else CurrentGitlab().project
    created_mr = project.mergerequests.create(
        {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            "description": description,
            "labels": list(labels),
            "remove_source_branch": not keep_source_branch,
        }
    )
    click.echo(f"✨ Successfully created MR #{created_mr.iid} : {created_mr.web_url}")
