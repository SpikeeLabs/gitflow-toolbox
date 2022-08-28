from parameterized import parameterized

from gitflow_toolbox.tests.testcases import GitflowTestCase


class GetProjectHttpUrlTests(GitflowTestCase):
    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_get_project_http_url(self, flag: str):
        result = self.runner.invoke(self.main_cli, ["get-project-http-url", flag], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "https://sample.spikeelabs.fr\n")
