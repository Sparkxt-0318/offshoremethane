"""Command-line entry point.

Phase 0 stub. Real subcommands are added in later phases:

    offshoreplume retrieve <scene-id>           # Phase 1
    offshoreplume scan <region>                  # Phase 4
    offshoreplume quantify <detection-id>        # Phase 5
"""

from __future__ import annotations

import sys

from . import __version__


def main(argv: list[str] | None = None) -> int:
    """Minimal CLI: only supports ``--version`` at Phase 0."""
    args = sys.argv[1:] if argv is None else argv
    if not args or args[0] in {"-h", "--help"}:
        print("offshoreplume CLI (Phase 0 stub)")
        print("Usage:")
        print("  offshoreplume --version")
        print("Subcommands (retrieve, scan, quantify) are added in later phases.")
        return 0
    if args[0] in {"-V", "--version"}:
        print(f"offshoreplume {__version__}")
        return 0
    print(f"Unknown argument: {args[0]!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
