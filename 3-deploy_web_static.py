#!/usr/bin/python3
# Full deployment
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['3.235.174.226', '44.210.106.28']


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder
    """
    date_now = datetime.now().strftime('%Y%m%d%H%M%S')
    local("mkdir -p versions/")
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(date_now))
        return "versions/web_static_{}.tgz".format(date_now)
    except Exception:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    """
    if not path.exists(archive_path):
        return False
    filename = archive_Path.split("/")[-1]
    rm_ext = filename.split(".")[0]
    folder = "/data/web_static/releases/{}/".format(rm_ext)
    symlink = "/data/web_static/current"

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, folder))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}web_static/* {}".format(folder, folder))
        run("sudo rm -rf {}web_static".format(folder))
        run("sudo rm -rf {}".format(symlink))
        run("sudo ln -s {} {}".format(folder, symlink))
        return True
    except Exception:
        return False


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    file_path = do_pack()
    if file_path is None:
        return False

    return (do_deploy(file_path))
