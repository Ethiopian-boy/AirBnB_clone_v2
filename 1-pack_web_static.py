#!/usr/bin/python3
# Compress before sending to .tgz
from datetime import datetime
from fabric.api import *


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
