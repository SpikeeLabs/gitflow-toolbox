from parameterized import parameterized

from gitflow_toolbox.tests.testcases import GitflowTestCase


class GetProjectSshUrlTests(GitflowTestCase):
    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_get_project_ssh_url(self, flag: str):
        result = self.runner.invoke(self.main_cli, ["get-project-ssh-url", flag], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "ssh_url_to_repo\n")
