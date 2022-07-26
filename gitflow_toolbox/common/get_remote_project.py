from gitlab.v4.objects.projects import Project

from gitflow_toolbox.common.get_env import get_env
from gitflow_toolbox.common.get_remote_gitlab import get_remote_gitlab


def get_remote_project() -> Project:
    """Get remote gitlab sdk project

    Returns:
        gitlab.Gitlab: remote gitlab project instance (or 'target', 'destination' gitlab project)
    """
    return get_remote_gitlab().projects.get(get_env("REMOTE_GITLAB_PROJECT_ID"))
