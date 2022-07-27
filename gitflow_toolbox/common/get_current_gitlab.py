import os

import gitlab

from gitflow_toolbox.common.get_env import get_env


def get_current_gitlab() -> gitlab.Gitlab:
    """Get current gitlab sdk instance

    Returns:
        gitlab.Gitlab: current gitlab instance (or 'source', 'from' gitlab)
    """
    # If running in a gitlab CI job
    if os.getenv("GITLAB_CI"):
        # Use provided token, if not available, use default token from job
        private_token = get_env("GITLAB_PRIVATE_TOKEN", "CI_JOB_TOKEN")
        return gitlab.Gitlab(get_env("CI_SERVER_URL"), private_token)

    return gitlab.Gitlab(get_env("GITLAB_URL"), get_env("GITLAB_PRIVATE_TOKEN"))
