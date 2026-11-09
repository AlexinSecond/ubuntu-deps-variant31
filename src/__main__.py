"""Stage 5: build, describe and draw ordinary package dependencies."""

import lzma
import subprocess
import sys

from .config import parse_config
from .graph import dependency_graph
from .repository import load_repository
from .visualize import ascii_tree, render_png, to_dot


def run(config):
    """Load metadata, traverse the graph and save both representations."""
    repo = load_repository(config)
    graph = dependency_graph(repo.graph, config.package,
                             config.max_depth, config.exclude)
    if config.ascii:
        print(ascii_tree(graph, config.package))
    missing = sorted(repo.external.intersection(graph))
    if missing:
        print("Not in this index: " + ", ".join(missing), file=sys.stderr)
    dot_path = render_png(to_dot(graph, repo, config.package), config.output)
    print(f"DOT: {dot_path.resolve()}")
    print(f"PNG: {config.output.resolve()}")
    print(f"Nodes: {len(graph)}, edges: {sum(map(len, graph.values()))}")


def main(argv=None):
    """Return 0 on success, 1 on runtime error, or argparse's 2 on misuse."""
    config = parse_config(argv)
    try:
        run(config)
    except (OSError, ValueError, lzma.LZMAError, EOFError,
            subprocess.SubprocessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
