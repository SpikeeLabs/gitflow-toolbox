import click
from dotenv import load_dotenv

from gitflow_toolbox.create_remote_branch import create_remote_branch

load_dotenv()


@click.group()
def cli():
    pass


cli.add_command(create_remote_branch)

if __name__ == "__main__":
    cli()
