import click
from dotenv import load_dotenv

from gitflow_toolbox.check_branch_exists import check_branch_exists
from gitflow_toolbox.check_mr_exists import check_mr_exists
from gitflow_toolbox.ensure_branch import ensure_branch
from gitflow_toolbox.ensure_mr import ensure_mr

load_dotenv()


@click.group()
def cli():
    pass


cli.add_command(check_branch_exists)
cli.add_command(ensure_branch)
cli.add_command(check_mr_exists)
cli.add_command(ensure_mr)

if __name__ == "__main__":
    cli()
