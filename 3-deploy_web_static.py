#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from datetime import datetime
from fabric.api import env, local, put, run
from os.path import exists

env.hosts = ['IP_WEB_01', 'IP_WEB_02']
created_archive = None


def do_pack():
    """Generate a timestamped .tgz archive of web_static."""
    try:
        local("mkdir -p versions")
        archive = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))
        print("Packing web_static to {}".format(archive))
        local("tar -cvzf {} web_static".format(archive))
        return archive
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
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


def deploy():
    """Create an archive and distribute it to the web servers."""
    global created_archive
    if created_archive is None:
        created_archive = do_pack()
    if created_archive is None:
        return False
    return do_deploy(created_archive)
