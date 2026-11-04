"""Stage 2: download an index and display direct dependencies."""

import lzma
import sys

from .config import parse_config
from .download import download_index
from .packages import parse_packages


def main(argv=None):
    """Print direct relations and return a clear status on failure."""
    config = parse_config(argv)
    try:
        if config.test_repo:
            raise ValueError("Test repositories are added in stage 3")
        repo = parse_packages(download_index(config.repo))
        if config.package not in repo.graph:
            raise ValueError(f"Package not found: {config.package}")
        print(f"Direct dependencies of {config.package}:")
        print(repo.relations.get(config.package, "") or "(none / virtual)")
        for name in sorted(repo.graph[config.package]):
            print(name)
    except (OSError, ValueError, lzma.LZMAError, EOFError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
