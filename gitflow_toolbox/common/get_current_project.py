import os

from gitlab.v4.objects.projects import Project

from gitflow_toolbox.common.get_current_gitlab import get_current_gitlab
from gitflow_toolbox.common.get_env import get_env


def get_current_project() -> Project:
    """Get current gitlab sdk project

    Returns:
        gitlab.Gitlab: current gitlab project instance (or 'source', 'from' gitlab project)
    """
    gitlab = get_current_gitlab()
    # If running in a gitlab CI job
    if os.getenv("GITLAB_CI"):
        # Use provided CI project, if not available, use project from current job
        project_id = get_env("GITLAB_PROJECT_ID", "CI_PROJECT_ID")
        return gitlab.projects.get(project_id)

    return gitlab.projects.get(get_env("GITLAB_PROJECT_ID"))
