"""Check valid options and errors for every configurable parameter."""

import contextlib
import io
import unittest

from src.config import parse_config


class ConfigTests(unittest.TestCase):
    """CLI parsing works without network access or side effects."""

    def test_defaults(self):
        """The package is required; other options have defaults."""
        config = parse_config(["--package", "bash"])
        self.assertEqual(config.max_depth, 3)
        self.assertEqual(len(config.dump().splitlines()), 7)

    def test_all_options(self):
        """All seven options can be supplied together."""
        config = parse_config([
            "--package", "A", "--repo", "examples/tree.json",
            "--test-repo", "--output", "output/test.png", "--ascii",
            "--max-depth", "0", "--exclude", "B",
        ])
        self.assertTrue(config.ascii and config.test_repo)
        self.assertEqual(config.max_depth, 0)
        self.assertEqual(config.exclude, "B")

    def test_invalid_parameters(self):
        """Each setting has an invalid-input demonstration."""
        cases = [
            ["--package", "bad/name"],
            ["--repo", "ftp://example.com/Packages"],
            ["--repo", "https://example.com/index.html"],
            ["--test-repo", "yes"], ["--ascii", "yes"],
            ["--output", "file.jpg"], ["--max-depth", "-1"],
            ["--max-depth", "101"], ["--max-depth", "abc"],
            ["--exclude", "\n"],
            ["--test-repo", "--package", "A", "--repo", "missing.json"],
        ]
        for args in cases:
            with self.subTest(args=args):
                self.check_invalid(args)

    def check_invalid(self, args):
        """Expect an argparse failure without cluttering test output."""
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                parse_config(["--package", "bash", *args])
            self.assertEqual(caught.exception.code, 2)

    def test_missing_package(self):
        """A missing required package is a usage error."""
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_config([])
