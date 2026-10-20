#!/usr/bin/python3
"""Fabric script that creates a compressed archive of web_static."""

from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Generate a .tgz archive from the web_static directory."""
    if not os.path.isdir("versions"):
        os.makedirs("versions")

    archive_name = "web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    archive_path = os.path.join("versions", archive_name)

    print("Packing web_static to {}".format(archive_path))

    result = local("tar -czvf {} web_static".format(archive_path), capture=False)

    if result.failed:
        return None

    print("web_static packed: {} -> {}Bytes".format(
        archive_path, os.path.getsize(archive_path)
    ))
    return archive_path
