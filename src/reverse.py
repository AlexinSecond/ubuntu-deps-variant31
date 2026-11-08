"""Reverse edges before using the same recursive DFS algorithm."""


def reverse_graph(graph):
    """Return package -> packages directly depending on it."""
    result = {name: set() for name in graph}
    for parent, children in graph.items():
        for child in children:
            result.setdefault(child, set()).add(parent)
    return result
