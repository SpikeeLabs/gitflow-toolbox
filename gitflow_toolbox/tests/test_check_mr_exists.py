import itertools

from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockMergeRequest, append_title
from gitflow_toolbox.tests.testcases import GitflowTestCase


class CheckMrExistsTests(GitflowTestCase):
    @parameterized.expand(
        append_title(
            itertools.product(
                ["--remote", "--current", "-r", "-c"], ["-s opened", "-s closed", "-s locked", "-s merged"]
            )
        )
    )
    def test_cli_check_mr_exist_success(self, _, remote: str, state: str):
        self.project_mock.mergerequests.reset_mock()
        self.project_mock.mergerequests.list.return_value = [MockMergeRequest()]

        result = self.runner.invoke(
            self.main_cli, ["check-mr-exists", "src", "dst", remote, *state.split(" ")], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "Checking if an opened merge request from src to dst exists...\nTrue\n")

        self.project_mock.mergerequests.list.assert_called_once_with(
            state=state.split(" ")[1], source_branch="src", target_branch="dst"
        )

    @parameterized.expand(
        append_title(
            itertools.product(
                ["--remote", "--current", "-r", "-c"], ["-s opened", "-s closed", "-s locked", "-s merged"]
            )
        )
    )
    def test_cli_check_mr_exist_failure(self, _, remote: str, state: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli, ["check-mr-exists", "src", "dst", remote, *state.split(" ")], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 1, result.output)
        self.assertEqual(result.output, "Checking if an opened merge request from src to dst exists...\nFalse\n")

        self.project_mock.mergerequests.list.assert_called_once_with(
            state=state.split(" ")[1], source_branch="src", target_branch="dst"
        )
