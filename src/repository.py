"""Load either real Ubuntu metadata or a local teaching graph."""

import json
import re
from pathlib import Path

from .config import TEST_NAME
from .download import download_index
from .packages import Repository, parse_packages


def unique_object(pairs):
    """Reject duplicate JSON keys instead of silently losing edges."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Repeated package: {key}")
        result[key] = value
    return result


def check_test_graph(graph):
    """Require an explicit list of dependencies for every named node."""
    if not isinstance(graph, dict) or not graph:
        raise ValueError("Test repository must be a nonempty JSON object")
    for name, children in graph.items():
        if not re.fullmatch(TEST_NAME, name):
            raise ValueError(f"Use uppercase Latin names: {name}")
        if not isinstance(children, list):
            raise ValueError(f"Expected a dependency list for {name}")
        for child in children:
            if not isinstance(child, str) or child not in graph:
                raise ValueError(f"Undeclared dependency in {name}: {child}")


def load_test_repo(path):
    """Read a UTF-8/BOM JSON adjacency list, preserving the input file."""
    text = Path(path).read_text(encoding="utf-8-sig")
    graph = json.loads(text, object_pairs_hook=unique_object)
    check_test_graph(graph)
    return Repository({name: set(children) for name, children in graph.items()})


def load_repository(config):
    """Select the data source requested by CLI settings."""
    if config.test_repo:
        return load_test_repo(config.repo)
    return parse_packages(download_index(config.repo))
