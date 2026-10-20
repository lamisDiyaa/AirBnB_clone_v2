#!/usr/bin/python3
"""Generates a .tgz archive from web_static."""
from datetime import datetime
from os.path import isdir, getsize
from subprocess import run


def do_pack():
    """Create a timestamped archive."""
    run(["mkdir", "-p", "versions"], check=True)
    archive_path = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    result = run(["tar", "-czf", archive_path, "web_static"])
    if result.returncode:
        return None
    print("web_static packed: {} -> {}Bytes".format(
        archive_path, getsize(archive_path)))
    return archive_path


if __name__ == "__main__":
    do_pack()
