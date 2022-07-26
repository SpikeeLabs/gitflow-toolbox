import click
from dotenv import load_dotenv

from gitflow_toolbox.check_branch_exists import check_branch_exists
from gitflow_toolbox.check_mr_exists import check_mr_exists
from gitflow_toolbox.diff import diff
from gitflow_toolbox.ensure_branch import ensure_branch
from gitflow_toolbox.ensure_mr import ensure_mr
from gitflow_toolbox.get_latest_mr_state import get_latest_mr_state
from gitflow_toolbox.get_project_http_url import get_project_http_url
from gitflow_toolbox.get_project_ssh_url import get_project_ssh_url
from gitflow_toolbox.push import push
from gitflow_toolbox.push_missing_tags import push_missing_tags

load_dotenv()


@click.group()
def cli():
    pass


cli.add_command(check_branch_exists)
cli.add_command(ensure_branch)
cli.add_command(check_mr_exists)
cli.add_command(ensure_mr)
cli.add_command(get_latest_mr_state)
cli.add_command(get_project_ssh_url)
cli.add_command(get_project_http_url)
cli.add_command(push)
cli.add_command(push_missing_tags)
cli.add_command(diff)

if __name__ == "__main__":
    cli()
