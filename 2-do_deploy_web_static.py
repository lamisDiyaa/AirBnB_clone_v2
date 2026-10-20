#!/usr/bin/python3
"""Distributes an archive to web servers."""

from fabric.api import env, put, run
from os.path import exists, basename, splitext

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Deploy an archive to the web servers."""
    if not exists(archive_path):
        return False

    archive_name = basename(archive_path)
    release_name = splitext(archive_name)[0]
    archive_tmp = "/tmp/{}".format(archive_name)
    release_path = "/data/web_static/releases/{}".format(release_name)
    current_link = "/data/web_static/current"

    try:
        put(archive_path, archive_tmp)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(archive_tmp, release_path))
        run("rm -f {}".format(archive_tmp))
        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf {}".format(current_link))
        run("ln -s {}/ {}".format(release_path, current_link))
        print("New version deployed!")
        return True
    except Exception:
        return False
