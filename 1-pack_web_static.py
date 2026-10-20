#!/usr/bin/python3
"""Generates a .tgz archive from web_static."""

from datetime import datetime
from fabric.api import local
from os.path import isdir, getsize


def do_pack():
    """Create a timestamped archive of web_static."""
    if not isdir("versions"):
        local("mkdir -p versions")

    archive_name = "web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to {}".format(archive_path))
    result = local("tar -czvf {} web_static".format(archive_path),
                   capture=False)

    if result.failed:
        return None

    print("web_static packed: {} -> {}Bytes".format(
        archive_path, getsize(archive_path)))
    return archive_path
