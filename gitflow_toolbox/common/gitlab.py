import os
import re

import gitlab
from gitlab.v4.objects.projects import Project

from gitflow_toolbox.common.get_env import get_env
from gitflow_toolbox.common.singleton import Singleton


class CurrentGitlab(gitlab.Gitlab, metaclass=Singleton):

    __project = None
    __private_token = None

    def __init__(self):
        self.__private_token = get_env("GITLAB_PRIVATE_TOKEN", "CI_JOB_TOKEN")
        super().__init__(get_env("GITLAB_URL", "CI_SERVER_URL"), self.__private_token)

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
                return self.__project

            # This line isn't covered by unit test to simplify singleton handling.
            self.__project = self.projects.get(get_env("GITLAB_PROJECT_ID"))  # pragma: no cover
        return self.__project

    @property
    def project_authenticated_url(self) -> str:
        return re.sub(
            r"^https?:\/\/", f"https://gitflow:{self.__private_token}@", self.project.attributes.get("http_url_to_repo")
        )


class RemoteGitlab(gitlab.Gitlab, metaclass=Singleton):

    __project = None
    __private_token = None

    def __init__(self):
        self.__private_token = get_env("REMOTE_GITLAB_PRIVATE_TOKEN", "GITLAB_PRIVATE_TOKEN", "CI_JOB_TOKEN")
        super().__init__(get_env("REMOTE_GITLAB_URL", "GITLAB_URL", "CI_SERVER_URL"), self.__private_token)

    @property
    def project(self) -> Project:
        """Get remote gitlab sdk project

        Returns:
            gitlab.Gitlab: remote gitlab project instance (or 'target', 'destination' gitlab project)
        """
        if not self.__project:
            self.__project = self.projects.get(
                get_env("REMOTE_GITLAB_PROJECT_ID", "GITLAB_PROJECT_ID", "CI_PROJECT_ID")
            )
        return self.__project

    @property
    def project_authenticated_url(self) -> str:
        return re.sub(
            r"^https?:\/\/", f"https://gitflow:{self.__private_token}@", self.project.attributes.get("http_url_to_repo")
        )
