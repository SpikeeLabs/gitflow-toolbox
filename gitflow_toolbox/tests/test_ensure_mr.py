from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockMergeRequest
from gitflow_toolbox.tests.testcases import GitflowTestCase


class EnsureMrTests(GitflowTestCase):
    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_mr_skip_already_exist(self, remote: str):
        self.project_mock.mergerequests.reset_mock()
        self.project_mock.mergerequests.list.return_value = [MockMergeRequest()]

        result = self.runner.invoke(
            self.main_cli, ["ensure-mr", "src", "dst", "title", "description", remote], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if an opened merge request from src to dst exists...\nMR already exists, nothing to do.\n",
        )

        self.project_mock.mergerequests.list.assert_called_once_with(
            state="opened", source_branch="src", target_branch="dst"
        )
        self.project_mock.mergerequests.create.assert_not_called()

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_mr_create(self, remote: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli, ["ensure-mr", "src", "dst", "title", "description", remote], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if an opened merge request from src to dst exists...\n"
            "MR does not exist, creating...\n"
            "✨ Successfully created MR #MR_ID : MR_URL\n",
        )

        self.project_mock.mergerequests.list.assert_called_once_with(
            state="opened", source_branch="src", target_branch="dst"
        )
        self.project_mock.mergerequests.create.assert_called_once_with(
            {
                "source_branch": "src",
                "target_branch": "dst",
                "title": "title",
                "description": "description",
                "labels": [],
                "remove_source_branch": True,
                "squash": False,
                "assignee_ids": 0,
                "reviewer_ids": 0,
            }
        )

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_mr_created_with_keep_source_branch_and_squash(self, remote: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli,
            ["ensure-mr", "src", "dst", "title", "description", remote, "--keep-source-branch", "--squash"],
            catch_exceptions=False,
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if an opened merge request from src to dst exists...\n"
            "MR does not exist, creating...\n"
            "✨ Successfully created MR #MR_ID : MR_URL\n",
        )

        self.project_mock.mergerequests.list.assert_called_once_with(
            state="opened", source_branch="src", target_branch="dst"
        )
        self.project_mock.mergerequests.create.assert_called_once_with(
            {
                "source_branch": "src",
                "target_branch": "dst",
                "title": "title",
                "description": "description",
                "labels": [],
                "remove_source_branch": False,
                "squash": True,
                "assignee_ids": 0,
                "reviewer_ids": 0,
            }
        )

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_mr_created_with_labels(self, remote: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli,
            ["ensure-mr", "src", "dst", "title", "description", "label1", "label2", remote],
            catch_exceptions=False,
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if an opened merge request from src to dst exists...\n"
            "MR does not exist, creating...\n"
            "✨ Successfully created MR #MR_ID : MR_URL\n",
        )

        self.project_mock.mergerequests.list.assert_called_once_with(
            state="opened", source_branch="src", target_branch="dst"
        )
        self.project_mock.mergerequests.create.assert_called_once_with(
            {
                "source_branch": "src",
                "target_branch": "dst",
                "title": "title",
                "description": "description",
                "labels": ["label1", "label2"],
                "remove_source_branch": True,
                "squash": False,
                "assignee_ids": 0,
                "reviewer_ids": 0,
            }
        )

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_ensure_mr_created_with_assignee_and_reviewer_ids(self, remote: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli,
            ["ensure-mr", "src", "dst", "title", "description", remote, "-ri", 1, "-ai", 1],
            catch_exceptions=False,
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.output,
            "Checking if an opened merge request from src to dst exists...\n"
            "MR does not exist, creating...\n"
            "✨ Successfully created MR #MR_ID : MR_URL\n",
        )

        self.project_mock.mergerequests.list.assert_called_once_with(
            state="opened", source_branch="src", target_branch="dst"
        )
        self.project_mock.mergerequests.create.assert_called_once_with(
            {
                "source_branch": "src",
                "target_branch": "dst",
                "title": "title",
                "description": "description",
                "labels": [],
                "remove_source_branch": True,
                "squash": False,
                "assignee_ids": [1],
                "reviewer_ids": [1],
            }
        )
