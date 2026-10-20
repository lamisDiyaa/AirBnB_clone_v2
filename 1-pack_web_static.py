#!/usr/bin/python3
"""Generates a .tgz archive from the contents of web_static."""
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generate a timestamped .tgz archive of web_static."""
    try:
        local("mkdir -p versions")
        archive = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf {} web_static".format(archive))
        return archive
    except Exception:
        return None
