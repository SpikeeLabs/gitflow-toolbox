import click


@click.command()
@click.argument("first", type=int)
@click.argument("second", type=int)
def cli(first: int, second: int) -> int:
    print(add(first, second))


def add(first: int, second: int) -> int:
    """Sample function

    Args:
        first (int): First integer
        second (int): Second integer

    Returns:
        int: Addition result
    """
    return first + second


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()  # pragma: no cover
