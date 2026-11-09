"""Verify finite trees, quoted DOT and real Graphviz rendering."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.packages import Repository
from src.visualize import ascii_tree, render_png, to_dot


class VisualizeTests(unittest.TestCase):
    """Visual output keeps graph information and reports renderer errors."""

    def test_ascii_cycle(self):
        """A back edge is shown once with a cycle marker."""
        tree = ascii_tree({"A": {"B"}, "B": {"A"}}, "A")
        self.assertEqual(tree, "A\n`-- B\n    `-- A [cycle]")

    def test_shared_subtree(self):
        """Shared nodes are cross-referenced instead of expanded again."""
        graph = {"A": {"B", "C"}, "B": {"D"}, "C": {"D"}, "D": set()}
        tree = ascii_tree(graph, "A")
        self.assertIn("D [shown above]", tree)

    def test_dot_is_deterministic(self):
        """Edges are sorted, names quoted and an isolated root preserved."""
        graph = {"aa-bb": {"cc"}, "cc": set()}
        text = to_dot(graph, Repository(graph), "aa-bb")
        self.assertIn('"aa-bb" -> "cc";', text)
        self.assertIn('"cc" [];', text)
        self.assertEqual(text, to_dot(graph, Repository(graph), "aa-bb"))

    def test_tree_uses_shortest_levels(self):
        """A longer route cannot make the displayed expansion too deep."""
        graph = {"A": {"B", "D"}, "B": {"C"}, "C": {"D"},
                 "D": {"E"}, "E": set()}
        tree = ascii_tree(graph, "A")
        self.assertIn("D [link]", tree)
        self.assertIn("`-- D\n    `-- E", tree)

    def test_virtual_and_missing_styles(self):
        """Virtual provider links and missing nodes are distinguished."""
        repo = Repository({"aa": {"bb"}, "bb": set()}, {"bb"}, {"aa"})
        text = to_dot(repo.graph, repo, "aa")
        self.assertIn('label="provider"', text)
        self.assertIn('color="red"', text)
        self.assertIn('shape=diamond', text)

    def test_missing_renderer_preserves_png(self):
        """DOT survives a renderer failure; the previous PNG stays intact."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "old.png"
            path.write_bytes(b"previous")
            with patch.dict(os.environ, {"GRAPHVIZ_DOT": "missing-dot-exe"}):
                with self.assertRaises(OSError):
                    render_png("digraph { A; }", path)
            self.assertEqual(path.read_bytes(), b"previous")
            self.assertTrue(path.with_suffix(".dot").is_file())

    def test_real_png(self):
        """Run the real renderer, including a destination with spaces."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "new folder" / "test.png"
            render_png("digraph { A -> B; }", path)
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
