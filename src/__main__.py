"""Stage 3: recursively build a dependency graph."""

import lzma
import sys

from .config import parse_config
from .graph import dependency_graph, edge_list
from .repository import load_repository


def main(argv=None):
    """Display the filtered graph, reporting source and traversal errors."""
    config = parse_config(argv)
    try:
        repo = load_repository(config)
        graph = dependency_graph(repo.graph, config.package,
                                 config.max_depth, config.exclude)
        print(edge_list(graph))
    except (OSError, ValueError, lzma.LZMAError, EOFError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
