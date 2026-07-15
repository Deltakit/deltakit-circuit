"""
Script to set the prerelease version number in the repository `pyproject.toml`.

Usage: `python -m tools.set_pre_version -t <secs_since_epoch> -c <short_commit_hash>`
Example: `python -m tools.set_pre_version -t 1734739200 -c abc1234`
"""

import argparse
import logging
from pathlib import Path
from packaging.version import Version


import tomlkit

# logging
stream_handler = logging.StreamHandler()
logger = logging.Logger(__name__)
logger.addHandler(stream_handler)


PROJ_HOME = Path(__file__).parents[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Append prerelease suffix to the base version."
    )
    parser.add_argument(
        "-t",
        "--timestamp",
        type=int,
        required=True,
        help="Prerelease version timestamp suffix (seconds since epoch).",
    )
    parser.add_argument(
        "-c",
        "--commit",
        required=True,
        help="Prerelease version short commit hash suffix.",
    )
    args = parser.parse_args()
    timestamp_version_suffix = args.timestamp
    commit_version_suffix = args.commit

    # Update project version with suffix
    path = PROJ_HOME / "pyproject.toml"

    # Update file data
    with path.open("r", encoding="utf-8") as f:
        data: dict = tomlkit.load(f)

    version = Version(data["project"]["version"])
    prerelease_version = f"{version.major}.{version.minor}.{version.micro + 1}"
    data["project"]["version"] = (
        prerelease_version +
        f".dev{timestamp_version_suffix}+g{commit_version_suffix}"
    )

    # Write updated data to file
    with path.open("w", encoding="utf-8") as f:
        tomlkit.dump(data, f)

    logger.info("Project successfully updated")
