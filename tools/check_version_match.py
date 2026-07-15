# (c) Copyright Riverlane 2020-2026. All rights reserved.
"""
Validates package version matches latest remote tag.
"""

import argparse
import logging
import sys

from tools.utils import extract_version

# logging
stream_handler = logging.StreamHandler()
logger = logging.Logger(__name__)
logger.addHandler(stream_handler)


SEMVER_PARTS: int = 3


def parse_version(v: str) -> tuple:
    """
    Parse a semantic version string.

    Args:
        v: Semantic version string in the format MAJOR.MINOR.PATCH.

    Returns:
        A tuple containing the major, minor, and patch version numbers.

    Raises:
        argparse.ArgumentTypeError: If v is not in the format
            MAJOR.MINOR.PATCH or contains non-integer components.
    """
    parts = v.split(".")
    if len(parts) != SEMVER_PARTS:
        msg = f"Invalid semver format: '{v}' (expected MAJOR.MINOR.PATCH)"
        raise argparse.ArgumentTypeError(msg)

    try:
        major, minor, patch = map(int, parts)
        return major, minor, patch
    except ValueError as err:
        msg = f"Invalid semver format: '{v}' (expected MAJOR.MINOR.PATCH)"
        raise argparse.ArgumentTypeError(msg) from err


def main():
    desc = "Check that the project version matches the provided version."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "version",
        type=parse_version,
        help="Version to compare against (format: MAJOR.MINOR.PATCH)",
    )

    args = parser.parse_args()
    tag_version_tup = args.version
    tag_version = ".".join(map(str, tag_version_tup))

    proj_version = extract_version()
    proj_version_tup = parse_version(proj_version)

    if proj_version_tup != tag_version_tup:
        logger.error(
            "Project version %s does not match latest tag version %s",
            proj_version,
            tag_version,
        )
        sys.exit(1)

    logger.info(
        "Project version %s matches latest tag version %s",
        proj_version,
        tag_version,
    )


if __name__ == "__main__":
    main()
