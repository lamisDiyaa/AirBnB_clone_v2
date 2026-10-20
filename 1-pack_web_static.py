#!/usr/bin/python3
"""Generates a .tgz archive from the contents of web_static."""

from datetime import datetime
from fabric.api import local
from os.path import exists, isdir, getsize


def do_pack():
    """Generate a .tgz archive of the web_static directory."""
    if not isdir("versions"):
        try:
            local("mkdir -p versions")
        except Exception:
            return None

    archive_name = "web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to {}".format(archive_path))
    result = local("tar -czvf {} web_static".format(archive_path),
                   capture=False)

    if result.failed or not exists(archive_path):
        return None

    print("web_static packed: {} -> {}Bytes".format(
        archive_path, getsize(archive_path)))
    return archive_path
