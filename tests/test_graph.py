"""Regression tests for recursive traversal and teaching repositories."""

import unittest

from src.graph import dependency_graph
from src.repository import check_test_graph, load_test_repo, unique_object


class GraphTests(unittest.TestCase):
    """Verify cycles, shared nodes, shortest depth and exclusions."""

    def test_depth_zero(self):
        """Depth zero contains only the requested root."""
        graph = load_test_repo("examples/tree.json").graph
        self.assertEqual(dependency_graph(graph, "A", 0), {"A": set()})

    def test_depth_one(self):
        """Direct dependencies are included without their children."""
        graph = load_test_repo("examples/tree.json").graph
        self.assertEqual(dependency_graph(graph, "A", 1),
                         {"A": {"B", "C"}, "B": set(), "C": set()})

    def test_cycle_terminates(self):
        """A back edge is retained without infinite recursion."""
        graph = load_test_repo("examples/cycle.json").graph
        self.assertEqual(dependency_graph(graph, "A", 10), graph)

    def test_shorter_path_reexpands(self):
        """A DFS node first reached at the limit can later be expanded."""
        graph = load_test_repo("examples/diamond.json").graph
        result = dependency_graph(graph, "A", 3)
        self.assertEqual(result["D"], {"E"})
        self.assertIn("E", result)

    def test_filter_prunes_branch(self):
        """Excluded packages and their otherwise unreachable children vanish."""
        graph = load_test_repo("examples/tree.json").graph
        self.assertEqual(dependency_graph(graph, "A", 10, "B"),
                         {"A": {"C"}, "C": set()})

    def test_substring_filter(self):
        """Filtering is a substring match, not just name equality."""
        graph = {"A": {"BB", "BC"}, "BB": set(), "BC": set()}
        self.assertEqual(dependency_graph(graph, "A", 10, "B"),
                         {"A": set()})

    def test_missing_or_filtered_root(self):
        """Invalid roots have a useful error rather than an empty graph."""
        for root, exclude in [("Z", ""), ("A", "A")]:
            with self.assertRaises(ValueError):
                dependency_graph({"A": set()}, root, 3, exclude)

    def test_disconnected_and_self_loop(self):
        """Unreachable nodes stay out; a self-loop remains visible."""
        self.assertEqual(dependency_graph({"A": {"A"}, "B": set()}, "A", 3),
                         {"A": {"A"}})

    def test_bad_test_repositories(self):
        """Unknown targets, wrong types and lowercase names are rejected."""
        cases = [{}, [], {"a": []}, {"A": "B"}, {"A": ["B"]}, {"A": [1]}]
        for graph in cases:
            with self.subTest(graph=graph), self.assertRaises(ValueError):
                check_test_graph(graph)

    def test_duplicate_json_keys(self):
        """Repeated nodes cannot silently replace earlier edges."""
        with self.assertRaises(ValueError):
            unique_object([("A", []), ("A", ["B"])])
