from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockBranch
from gitflow_toolbox.tests.testcases import GitflowTestCase


class EnsureBranchTests(GitflowTestCase):
    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_branch_skip_branch_already_exist(self, flag: str):
        self.project_mock.branches.reset_mock()
        self.project_mock.branches.list.return_value = [MockBranch("dst")]

        result = self.runner.invoke(self.main_cli, ["ensure-branch", "dst", "src", flag], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "Checking if dst branch exists...\nBranch already exists, nothing to do.\n")

        self.project_mock.branches.list.assert_called_once_with()
        self.project_mock.branches.create.assert_not_called()

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_branch_create_missing_branch(self, flag: str):
        self.project_mock.branches.reset_mock()

        result = self.runner.invoke(self.main_cli, ["ensure-branch", "dst", "src", flag], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if dst branch exists...\n"
            "Branch does not exist, creating...\n"
            "✨ Successfully created branch dst from src\n",
        )

        self.project_mock.branches.list.assert_called_once_with()
        self.project_mock.branches.create.assert_called_once_with({"branch": "dst", "ref": "src"})
