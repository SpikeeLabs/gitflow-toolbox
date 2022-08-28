import itertools

from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockMergeRequest, append_title
from gitflow_toolbox.tests.testcases import GitflowTestCase


class GetLatestMrStateTests(GitflowTestCase):
    @parameterized.expand(
        append_title(itertools.product(["--remote", "--current", "-r", "-c"], ["opened", "closed", "merged", "locked"]))
    )
    def test_cli_get_latest_mr_state_mr_found(self, _, flag: str, state: str):
        self.project_mock.mergerequests.reset_mock()
        self.project_mock.mergerequests.list.return_value = [MockMergeRequest(state=state)]

        result = self.runner.invoke(
            self.main_cli, ["get-latest-mr-state", "src", "dst", "label1", flag], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, f"{state}\n")

        self.project_mock.mergerequests.list.assert_called_once_with(
            source_branch="src", target_branch="dst", order_by="created_at", labels=["label1"]
        )

    @parameterized.expand(["--remote", "--current", "-r", "-c"])
    def test_cli_get_latest_mr_state_return_no_mr(self, flag: str):
        self.project_mock.mergerequests.reset_mock()

        result = self.runner.invoke(
            self.main_cli, ["get-latest-mr-state", "src", "dst", "label1", flag], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "no-mr\n")

        self.project_mock.mergerequests.list.assert_called_once_with(
            source_branch="src", target_branch="dst", order_by="created_at", labels=["label1"]
        )

    @parameterized.expand(
        append_title(itertools.product(["--remote", "--current", "-r", "-c"], ["opened", "closed", "merged", "locked"]))
    )
    def test_cli_get_latest_mr_state_multiples_mr_found_return_state_of_first_found(self, _, flag: str, state: str):
        self.project_mock.mergerequests.reset_mock()
        self.project_mock.mergerequests.list.return_value = [
            MockMergeRequest(state=state),
            MockMergeRequest(state="opened"),
        ]

        result = self.runner.invoke(
            self.main_cli, ["get-latest-mr-state", "src", "dst", "label1", flag], catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, f"{state}\n")

        self.project_mock.mergerequests.list.assert_called_once_with(
            source_branch="src", target_branch="dst", order_by="created_at", labels=["label1"]
        )
