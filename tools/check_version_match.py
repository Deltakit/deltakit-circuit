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


def parse_version(v: str) -> tuple:
    """Takes a semver and returns a version as tuple.

    Args:
      v: Semantic version.

    Raise:
      ValueError if the semver format is not supported.

    Returns:
      A semver as a tuple
    """
    try:
        return tuple(map(int, v.split(".")))
    except ValueError as err:
        msg = f"Invalid semver format: '{v}' (expected MAJOR.MINOR.PATCH)"
        raise argparse.ArgumentTypeError(msg) from err


def main():
    desc = "Check that the project version is higher than the provided version."
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
        log_msg = (
            f"Project version {proj_version} do not match "
            f"latest tag version {tag_version_tup}."
        )
        logger.error(log_msg)
        sys.exit(1)

    logger.info(
        "Project version %s do not match latest tag version %s",
        proj_version,
        tag_version,
    )


if __name__ == "__main__":
    main()
