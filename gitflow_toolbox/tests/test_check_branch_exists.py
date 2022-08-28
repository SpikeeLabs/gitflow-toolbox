from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockBranch
from gitflow_toolbox.tests.testcases import GitflowTestCase


class CheckBranchExistsTests(GitflowTestCase):
    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_check_branch_exist_success(self, flag: str):
        self.project_mock.branches.reset_mock()
        self.project_mock.branches.list.return_value = [MockBranch("target_branch")]

        result = self.runner.invoke(
            self.main_cli, ["check-branch-exists", "target_branch", flag], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "Checking if target_branch branch exists...\nTrue\n")

        self.project_mock.branches.list.assert_called_once_with()

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_check_branch_exist_failure(self, flag: str):
        self.project_mock.branches.reset_mock()

        result = self.runner.invoke(
            self.main_cli, ["check-branch-exists", "target_branch", flag], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 1, result.output)
        self.assertEqual(result.output, "Checking if target_branch branch exists...\nFalse\n")

        self.project_mock.branches.list.assert_called_once_with()
