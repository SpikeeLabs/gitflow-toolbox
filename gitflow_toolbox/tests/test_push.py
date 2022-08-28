import itertools
from unittest import mock

from parameterized import parameterized

from gitflow_toolbox.tests.factories import DictObject, MockGitRepo, append_title
from gitflow_toolbox.tests.testcases import GitflowTestCase


class PushTests(GitflowTestCase):
    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_push_successful(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.create_remote("target")
            mock_repo.create_remote.reset_mock()
            mock_repo.remotes.target.push.return_value = [DictObject(summary="Some change")]

            result = self.runner.invoke(
                self.main_cli, ["push", "src", "dst", flag_key, flag_val], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(result.output)

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.remotes.target.push.assert_called_once_with(refspec="src:dst", force=False)

    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_push_failure(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.create_remote("target")
            mock_repo.create_remote.reset_mock()
            mock_repo.remotes.target.push.return_value = [DictObject(summary="rejected")]

            result = self.runner.invoke(
                self.main_cli, ["push", "src", "dst", flag_key, flag_val], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 1, result.output)
            self.assertTrue(result.output)
            self.assertIn("❌ Couldn't push changes to", result.output)

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.remotes.target.push.assert_called_once_with(refspec="src:dst", force=False)

    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_push_successful_with_force_option(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.create_remote("target")
            mock_repo.create_remote.reset_mock()
            mock_repo.remotes.target.push.return_value = [DictObject(summary="Some change")]

            result = self.runner.invoke(
                self.main_cli, ["push", "src", "dst", flag_key, flag_val, "-f"], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertTrue(result.output)
            self.assertIn("✨ Successfully pushed", result.output)

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.remotes.target.push.assert_called_once_with(refspec="src:dst", force=True)

    @parameterized.expand(
        append_title(itertools.product(["--from-gitlab", "--to-gitlab", "-t"], ["current", "remote"]))
    )
    def test_push_failure_with_force_option(self, _, flag_key: str, flag_val: str):
        with mock.patch("git.Repo.clone_from") as mock_clone_repo:
            mock_repo = MockGitRepo()
            mock_clone_repo.return_value = mock_repo
            mock_repo.create_remote("target")
            mock_repo.create_remote.reset_mock()
            mock_repo.remotes.target.push.return_value = [DictObject(summary="rejected")]

            result = self.runner.invoke(
                self.main_cli, ["push", "src", "dst", flag_key, flag_val, "-f"], catch_exceptions=False
            )
            self.assertEqual(result.exit_code, 1, result.output)
            self.assertTrue(result.output)
            self.assertIn("❌ Couldn't push changes to", result.output)

            mock_clone_repo.assert_called_once()
            mock_repo.create_remote.assert_called_once()
            mock_repo.remotes.target.fetch.assert_called_once_with("dst")
            mock_repo.remotes.target.push.assert_called_once_with(refspec="src:dst", force=True)
