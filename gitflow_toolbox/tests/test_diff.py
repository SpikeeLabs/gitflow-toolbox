import itertools
from unittest import mock

from parameterized import parameterized

from gitflow_toolbox.tests.factories import MockGitRepo, append_title
from gitflow_toolbox.tests.testcases import GitflowTestCase


class DiffTests(GitflowTestCase):
    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "-f", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_diff_successful(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.git.diff.return_value = "diff"

            result = self.runner.invoke(
                self.main_cli, ["diff", "src", "dst", flag_key, flag_val], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(result.output, "diff\n")

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.git.diff.assert_called_once()

    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "-f", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_when_no_diff(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.git.diff.return_value = ""

            result = self.runner.invoke(
                self.main_cli, ["diff", "src", "dst", flag_key, flag_val], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(result.output, "")

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.git.diff.assert_called_once()
