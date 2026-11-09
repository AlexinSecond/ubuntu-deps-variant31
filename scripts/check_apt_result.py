"""Compare direct metadata dependencies with independent apt-cache output."""

import re
import sys
from pathlib import Path

from src.packages import parse_packages

IMPORTANT = re.compile(r"^\s*\|?(?:PreDepends|Pre-Depends|Depends):\s*<?"
                       r"([a-z0-9][a-z0-9+.-]+)", re.MULTILINE)


def compare_package(folder, repo, name):
    """Compare important dependencies and describe extra DOT relations."""
    text = (folder / f"{name}-apt.txt").read_text(encoding="utf-8")
    actual = set(IMPORTANT.findall(text))
    expected = repo.graph[name]
    dot = (folder / f"{name}-apt.dot").read_text(encoding="utf-8")
    edges = set(re.findall(r'"' + re.escape(name) + r'"\s*->\s*"([^"]+)"',
                           dot))
    if not expected <= edges:
        raise ValueError(f"APT DOT missing expected links for {name}")
    if actual != expected:
        raise ValueError(f"{name}: metadata={expected}, apt={actual}")
    lines = [f"{name}: direct dependencies match",
             "  " + ", ".join(sorted(actual)),
             "  Extra APT DOT targets: " + ", ".join(sorted(edges - actual))]
    return "\n".join(lines)


def main():
    """Write a reproducible comparison report, failing on mismatches."""
    folder = Path(sys.argv[1])
    index = next((folder / "lists").glob("*_Packages"))
    repo = parse_packages(index.read_text(encoding="utf-8"))
    results = [compare_package(folder, repo, name)
               for name in ("bash", "grep", "sed")]
    report = "\n\n".join(results) + "\n"
    (folder / "comparison.txt").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
