"""Stage 1: display the validated configuration."""

from .config import parse_config


def main(argv=None):
    """Print all seven user-configurable parameters."""
    print(parse_config(argv).dump())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
