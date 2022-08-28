import itertools
from unittest import mock

from parameterized import parameterized

from gitflow_toolbox.tests.factories import DictObject, MockGitRepo, append_title
from gitflow_toolbox.tests.testcases import GitflowTestCase


class PushMissingTagsTests(GitflowTestCase):
    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "--to-gitlab", "-t", "-f"], ["current", "remote"]))
    )
    def test_push_missing_tags_successful(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo_from = MockGitRepo()
            mock_repo_to = MockGitRepo()
            mock_clone_repo.side_effect = [mock_repo_from, mock_repo_to]
            mock_repo_from.create_remote("target")
            mock_repo_from.create_remote.reset_mock()
            mock_repo_from.tags.__iter__.return_value = [DictObject(name="tag-to-push")]
            mock_repo_to.tags.__iter__.return_value = []

            result = self.runner.invoke(
                self.main_cli, ["push-missing-tags", flag_key, flag_val], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(result.output)

            mock_clone_repo.assert_called()
            self.assertEqual(mock_clone_repo.call_count, 2)
            mock_repo_from.tags.__iter__.assert_called_once()
            mock_repo_to.tags.__iter__.assert_called_once()
            mock_repo_from.create_remote.assert_called_once()
            mock_repo_from.remotes.target.fetch.assert_called_once_with()
            # mock_repo_from.remotes.target.push.assert_called()
