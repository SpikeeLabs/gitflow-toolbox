from unittest import TestCase

from click.testing import CliRunner

from gitflow_toolbox.sample import add, cli


class SampleTests(TestCase):
    def test_add(self):
        self.assertEqual(add(1, 1), 2)

    def test_add_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["1", "1"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "2\n")
