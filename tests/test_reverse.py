"""Check reverse edges and recursive reverse traversal."""

import unittest

from src.graph import dependency_graph
from src.repository import load_test_repo
from src.reverse import reverse_graph


class ReverseTests(unittest.TestCase):
    """The stage 3 algorithm also works on inverted edges."""

    def test_reverse_chain(self):
        """D is needed by B, which is needed by A."""
        source = load_test_repo("examples/tree.json").graph
        graph = dependency_graph(reverse_graph(source), "D", 3)
        self.assertEqual(graph, {"D": {"B"}, "B": {"A"}, "A": set()})

    def test_reverse_depth(self):
        """Depth one shows only direct consumers."""
        source = load_test_repo("examples/tree.json").graph
        self.assertEqual(dependency_graph(reverse_graph(source), "D", 1),
                         {"D": {"B"}, "B": set()})

    def test_reverse_cycle(self):
        """Cycles are retained and do not prevent termination."""
        source = load_test_repo("examples/cycle.json").graph
        graph = dependency_graph(reverse_graph(source), "A", 10)
        self.assertEqual(graph, {"A": {"C"}, "C": {"B"}, "B": {"A"}})

    def test_no_consumers(self):
        """A package without consumers is still shown."""
        source = load_test_repo("examples/tree.json").graph
        self.assertEqual(dependency_graph(reverse_graph(source), "A", 3),
                         {"A": set()})

    def test_reverse_filter(self):
        """The filter also prunes reverse traversal branches."""
        source = load_test_repo("examples/tree.json").graph
        result = dependency_graph(reverse_graph(source), "D", 3, "B")
        self.assertEqual(result, {"D": set()})
