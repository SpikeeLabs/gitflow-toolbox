import click


def is_main_call(ctx: click.Context) -> bool:
    """Returns true if the current click function call is the main call

    Args:
        ctx (click.Context): current context
    """
    return ctx.parent.info_name == "main.py"
