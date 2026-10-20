#!/usr/bin/python3
"""Generates a .tgz archive from web_static."""
from datetime import datetime
from os.path import isdir, getsize
from subprocess import run


def do_pack():
    """Create a timestamped archive."""
    if not isdir("versions"):
        run(["mkdir", "-p", "versions"], check=True)
    archive = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S"))
    result = run(["tar", "-czf", archive, "-C", ".", "web_static"])
    if result.returncode != 0:
        return None
    print("web_static packed: {} -> {}Bytes".format(archive, getsize(archive)))
    return archive


if __name__ == "__main__":
    do_pack()
