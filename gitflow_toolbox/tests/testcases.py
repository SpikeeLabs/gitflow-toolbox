from importlib import import_module
from unittest import TestCase, mock

from click.testing import CliRunner

from gitflow_toolbox.tests.factories import MockProject

# This object MUST be declared globally to prevent error between tests using the
# `GitflowTestCase`, or the Project in `RemoteGitlab` and `CurrentGitlab` caches
# will be deleted and regenerated with an unknown pointer for tests.
PROJECT = MockProject()


class GitflowTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.main_cli = import_module("main").cli
        cls.main_cli.name = "main.py"

        cls.project_get_mock = mock.patch("gitlab.v4.objects.projects.ProjectManager.get").start()
        cls.project_mock = PROJECT
        cls.project_get_mock.return_value = cls.project_mock

    def setUp(self) -> None:
        super().setUp()

        # Setup env vars to prevent raise during `CurrentGitlab` and `RemoteGitlab` usages
        self.runner = CliRunner(
            env={
                "REMOTE_GITLAB_PRIVATE_TOKEN": "REMOTE_GITLAB_PRIVATE_TOKEN",
                "REMOTE_GITLAB_URL": "REMOTE_GITLAB_URL",
                "REMOTE_GITLAB_PROJECT_ID": "REMOTE_GITLAB_PROJECT_ID",
                "GITLAB_PRIVATE_TOKEN ": "GITLAB_PRIVATE_TOKEN ",
                "GITLAB_URL": "GITLAB_URL",
                "GITLAB_PROJECT_ID": "GITLAB_PROJECT_ID",
                "CI_JOB_TOKEN": "CI_JOB_TOKEN",
                "GITLAB_CI": "GITLAB_CI",
            }
        )
