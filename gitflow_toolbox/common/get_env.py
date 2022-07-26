import os


def get_env(*argv: str) -> str:
    """Returns the first env var value found in the given list of env var names.

    Args:
        argv (str): list of env vars to search for

    Raises:
        Exception: if no value is found

    Returns:
        str: env var value
    """
    for arg in argv:
        val = os.getenv(arg)
        if val is not None:
            return val
    if len(argv) == 1:
        raise Exception(f"env var {argv[0]} is not set")
    raise Exception(f"none of {argv} env var is set")
