import itertools
from functools import reduce
from typing import Union
from unittest import mock


class DictObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MockBranch:
    def __init__(self, name: str = "BRANCH") -> None:
        self.name = name


class MockMergeRequest:
    def __init__(self, iid: str = "MR_ID", web_url: str = "MR_URL", state: str = "opened") -> None:
        self.iid = iid
        self.web_url = web_url
        self.state = state


class MockBranchManager:
    def __init__(self) -> None:
        self.list = mock.MagicMock()
        self.list.return_value = []
        self.create = mock.MagicMock()

    def reset_mock(self):
        self.list.reset_mock()
        self.create.reset_mock()
        self.list.return_value = []


class MockMergeRequestManager:
    def __init__(self) -> None:
        self.list = mock.MagicMock()
        self.list.return_value = []
        self.create = mock.MagicMock()
        self.create.return_value = MockMergeRequest()

    def reset_mock(self):
        self.list.reset_mock()
        self.create.reset_mock()
        self.list.return_value = []
        self.create.return_value = MockMergeRequest()


class MockProject:
    def __init__(self) -> None:
        self.branches = MockBranchManager()
        self.mergerequests = MockMergeRequestManager()
        self.attributes = {
            "http_url_to_repo": "https://sample.spikeelabs.fr",
            "ssh_url_to_repo": "ssh_url_to_repo",
        }


class MockGitRemoteInstance:
    def __init__(self) -> None:
        self.fetch = mock.MagicMock()
        self.push = mock.MagicMock()


class MockGitRemote:
    def __init__(self) -> None:
        self.fetch = mock.MagicMock()

    def reset(self):
        self.fetch.reset_mock()

    def create_remote(self, *args, **kwargs):  # pylint: disable=W0613
        if not hasattr(self, args[0]):
            setattr(self, args[0], MockGitRemoteInstance())


class MockGitGit:
    def __init__(self) -> None:
        self.diff = mock.MagicMock()
        self.diff.return_value = None

    def reset(self):
        self.diff.reset_mock()
        self.diff.return_value = None


class MockGitRepo:
    def __init__(self) -> None:
        self.create_remote = mock.MagicMock()
        self.remotes = MockGitRemote()
        self.git = MockGitGit()
        self.tags = mock.MagicMock()

        self.create_remote.side_effect = self.__create_remote

    def reset(self):
        self.create_remote.reset_mock()
        self.remotes.reset()
        self.git.reset()
        self.tags.reset_mock()

    def __create_remote(self, *args, **kwargs):
        self.remotes.create_remote(*args, **kwargs)


def append_title(*args: Union[str, list[str]]):
    """This is just an utils to rewrite title of test when we use parameterized.expend

    It help use to understand which case of expended tests fail.

    Yields:
        Union[str, list[str]: Given argument rewrite properly
    """
    if args and isinstance(args[0], itertools.product):
        args = args[0]

    for arg in list(args):
        if isinstance(arg, tuple):
            arg = list(arg)
        if isinstance(arg, list):
            arg.insert(0, reduce(lambda x, y: f"{x.replace('-', '')}_{y.replace('-', '')}", arg))
        if isinstance(arg, str):
            arg = arg.replace("-", "")

        yield arg
