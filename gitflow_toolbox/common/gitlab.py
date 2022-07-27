import os

import gitlab
from gitlab.v4.objects.projects import Project

from gitflow_toolbox.common.get_env import get_env
from gitflow_toolbox.common.singleton import Singleton


class CurrentGitlab(gitlab.Gitlab, metaclass=Singleton):

    __project = None

    def __init__(self):
        # If running in a gitlab CI job
        if os.getenv("GITLAB_CI"):
            # Use provided token, if not available, use default token from job
            private_token = get_env("GITLAB_PRIVATE_TOKEN", "CI_JOB_TOKEN")
            super().__init__(get_env("CI_SERVER_URL"), private_token)
        else:
            super().__init__(get_env("GITLAB_URL"), get_env("GITLAB_PRIVATE_TOKEN"))

    @property
    def project(self) -> Project:
        """Get current gitlab sdk project

        Returns:
            gitlab.Gitlab: current gitlab project instance (or 'source', 'from' gitlab project)
        """
        if not self.__project:
            # If running in a gitlab CI job
            if os.getenv("GITLAB_CI"):
                # Use provided CI project, if not available, use project from current job
                project_id = get_env("GITLAB_PROJECT_ID", "CI_PROJECT_ID")
                self.__project = self.projects.get(project_id)

            self.__project = self.projects.get(get_env("GITLAB_PROJECT_ID"))
        return self.__project


class RemoteGitlab(gitlab.Gitlab, metaclass=Singleton):

    __project = None

    def __init__(self):
        super().__init__(get_env("REMOTE_GITLAB_URL"), get_env("REMOTE_GITLAB_PRIVATE_TOKEN"))

    @property
    def project(self) -> Project:
        """Get remote gitlab sdk project

        Returns:
            gitlab.Gitlab: remote gitlab project instance (or 'target', 'destination' gitlab project)
        """
        if not self.__project:
            self.__project = self.projects.get(get_env("REMOTE_GITLAB_PROJECT_ID"))
        return self.__project
