from parameterized import parameterized

from gitflow_toolbox.common.get_env import get_env
from gitflow_toolbox.common.gitlab import CurrentGitlab, RemoteGitlab
from gitflow_toolbox.tests.testcases import GitflowTestCase


class CommonTests(GitflowTestCase):
    def test_get_env_raise_not_set_1_arg(self):
        self.assertRaises(Exception, lambda: get_env("FIRST"))

    def test_get_env_raise_not_set_3_args(self):
        self.assertRaises(Exception, lambda: get_env("FIRST", "SECOND", "THIRD"))

    def test_current_gitlab_project_authenticated_url(self):
        self.assertEqual(CurrentGitlab().project_authenticated_url, "https://gitflow:CI_JOB_TOKEN@sample.spikeelabs.fr")

    def test_remote_gitlab_project_authenticated_url(self):
        self.assertEqual(
            RemoteGitlab().project_authenticated_url, "https://gitflow:REMOTE_GITLAB_PRIVATE_TOKEN@sample.spikeelabs.fr"
        )
