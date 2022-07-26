import gitlab

from gitflow_toolbox.common.get_env import get_env


def get_remote_gitlab() -> gitlab.Gitlab:
    """Get remote gitlab sdk instance

    Returns:
        gitlab.Gitlab: remote gitlab instance (or 'target', 'destination' gitlab)
    """
    return gitlab.Gitlab(get_env("REMOTE_GITLAB_URL"), get_env("REMOTE_GITLAB_PRIVATE_TOKEN"))
