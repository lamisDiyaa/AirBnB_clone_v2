#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['حطي_IP_ويب_01', 'حطي_IP_ويب_02']


def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Returns True if all operations succeed, otherwise False.
    """
    if not exists(archive_path):
        return False
    file_name = archive_path.split("/")[-1]
    name = file_name.split(".")[0]
    path = "/data/web_static/releases/{}/".format(name)
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}web_static/* {0}".format(path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print("New version deployed!")
        return True
    except Exception:
        return False
