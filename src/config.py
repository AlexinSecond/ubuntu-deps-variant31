"""Parse and validate the seven command-line settings."""

import argparse
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_REPO = (
    "https://archive.ubuntu.com/ubuntu/dists/noble/"
    "main/binary-amd64/Packages.xz"
)
MAX_DEPTH = 100
APT_NAME = r"[a-z0-9][a-z0-9+.-]+"
TEST_NAME = r"[A-Z]+"


@dataclass(frozen=True)
class Config:
    """User settings; graph depth counts edges from the root."""

    package: str
    repo: str
    test_repo: bool
    output: Path
    ascii: bool
    max_depth: int
    exclude: str

    def dump(self):
        """Return all settings in key=value form."""
        values = asdict(self).items()
        return "\n".join(f"{key}={value}" for key, value in values)


def check_source(value, test_repo):
    """Require a readable file or an HTTP(S) Packages index URL."""
    if test_repo:
        with Path(value).open("rb"):
            return
    url = urlparse(value)
    if url.scheme not in {"https", "http"} or not url.hostname:
        raise ValueError("--repo: use an http(s) URL")
    names = ("Packages", "Packages.gz", "Packages.xz", "/")
    if not url.path.endswith(names):
        raise ValueError("--repo: use Packages[.gz/.xz] or its directory")
    if url.username or url.password or url.fragment:
        raise ValueError("--repo: credentials and fragments are unsupported")
    if any(char.isspace() for char in value):
        raise ValueError("--repo: URL contains whitespace")


def check_output(output, repo):
    """Reject invalid destinations without creating any files."""
    if output.suffix.lower() != ".png" or output.is_dir():
        raise ValueError("--output: specify a PNG file")
    if output.resolve() == Path(repo).resolve():
        raise ValueError("--output: cannot overwrite the input")
    for parent in output.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError("--output: parent path is a file")


def validate(config):
    """Validate names, paths, flags, filter and safe recursion depth."""
    pattern = TEST_NAME if config.test_repo else APT_NAME
    if not re.fullmatch(pattern, config.package):
        raise ValueError("--package: invalid package name for this mode")
    if not 0 <= config.max_depth <= MAX_DEPTH:
        raise ValueError(f"--max-depth: expected 0..{MAX_DEPTH}")
    if any(ord(char) < ord(" ") for char in config.exclude):
        raise ValueError("--exclude: control characters are unsupported")
    check_source(config.repo, config.test_repo)
    check_output(config.output, config.repo if config.test_repo else "")


def parse_config(argv=None):
    """Parse CLI options and report invalid values through argparse."""
    parser = argparse.ArgumentParser(description="Ubuntu dependency viewer")
    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--test-repo", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("output/graph.png"))
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--exclude", default="")
    config = Config(**vars(parser.parse_args(argv)))
    try:
        validate(config)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return config
