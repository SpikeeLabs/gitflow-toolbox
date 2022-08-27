import click

from gitflow_toolbox.check_mr_exists import check_mr_exists
from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab


@click.command()
@click.argument("source_branch", type=str)
@click.argument("target_branch", type=str)
@click.argument("title", type=str)
@click.argument("description", type=str)
@click.argument("labels", type=str, nargs=-1)
@click.option(
    "--keep-source-branch",
    "-ksb",
    is_flag=True,
    help="Flag used to specify that you want to keep the source branch once the merge request has been accepted",
)
@click.option(
    "--squash",
    "-s",
    is_flag=True,
    help="Flag used to specify that you want to squash commit when the merge request is accepted."
    " This is an option of Gitlab which could be manually deactivated by user after the merge request creation.",
)
@click.option(
    "--remote/--current",
    "-r/-c",
    default=False,
    help="Flag which allow you to chose between configured target or remote to run this tool."
    " By default, the script use --current flag.",
)
@click.option(
    "--assignee_ids",
    "-ai",
    type=int,
    multiple=True,
    help="Flag (accepting multiple values) used to specify the assignee IDs to set while creating the merge request.",
)
@click.option(
    "--reviewer_ids",
    "-ri",
    type=int,
    multiple=True,
    help="Flag (accepting multiple values) used to specify the reviewer IDs to set while creating the merge request.",
)
@click.pass_context
def ensure_mr(
    ctx: click.Context,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str = None,
    labels: tuple[str] = None,
    keep_source_branch: bool = False,
    squash: bool = False,
    remote: bool = False,
    assignee_ids: tuple[int] = 0,
    reviewer_ids: tuple[int] = 0,
):
    """Create a merge request from SOURCE_BRANCH to TARGET_BRANCH if not exists using given TITLE and DESCRIPTION \f

    Args:
        source_branch (str): branch to create
        target_branch (str): branch reference to create branch from
        title (str): MR title
        description (str, optional): MR description. Defaults to None.
        labels (tuple[str], optional): MR labels. Defaults to [].
        keep_source_branch (bool): if you want to keep source branch or not
        squash (bool): if you want to squash commits when MR is merged
        remote (bool, optional):
            whether to check on the current gitlab or remote gitlab (True=remote). Default to False.
        assignee_ids (tuple[int], optional): MR assignee IDs. Defaults to 0.
        reviewer_ids (tuple[int], optional): MR reviewer IDs. Defaults to 0.
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
            "labels": list(labels) if labels else [],
            "remove_source_branch": not keep_source_branch,
            "squash": squash,
            "assignee_ids": list(assignee_ids) if assignee_ids else 0,
            "reviewer_ids": list(reviewer_ids) if reviewer_ids else 0,
        }
    )
    click.echo(f"✨ Successfully created MR #{created_mr.iid} : {created_mr.web_url}")
