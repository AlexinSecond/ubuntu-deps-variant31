"""Demonstrate invalid values for all seven required CLI parameters."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USAGE_ERROR_CODE = 2


def main():
    """Display each error and fail if invalid input is unexpectedly accepted."""
    cases = [
        ["--package", "bad/name"],
        ["--repo", "ftp://example.com/Packages"],
        ["--test-repo", "yes"],
        ["--output", "graph.jpg"],
        ["--ascii", "yes"],
        ["--max-depth", "-1"],
        ["--exclude", "\n"],
    ]
    for arguments in cases:
        print(f"\nInvalid input: {arguments!r}", flush=True)
        command = [sys.executable, "-m", "src", "--package", "bash"]
        result = subprocess.run(command + arguments, cwd=ROOT, check=False)
        if result.returncode != USAGE_ERROR_CODE:
            raise SystemExit("Expected usage error with exit code 2")
    print("All seven invalid inputs were rejected.")


if __name__ == "__main__":
    main()
