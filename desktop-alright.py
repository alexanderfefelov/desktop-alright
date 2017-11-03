#!/usr/bin/env python

import io
import os
import sys
from os.path import expanduser
from subprocess import call
from subprocess import check_output


def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    if sys.argv[1] == ACTION_SAVE:
        save()
    elif sys.argv[1] == ACTION_RESTORE:
        restore()
    else:
        print_usage()
        sys.exit(1)


def save():
    desktop_dir = get_desktop_dir()
    data = []
    for entry in os.listdir(desktop_dir):
        path = os.path.join(desktop_dir, entry)
        info = check_output([CMD_GVFS_INFO, "-a", ATTR_ICON_POSITION, path]).splitlines()
        nemo_icon_position = filter(lambda x: ATTR_ICON_POSITION in x, info)[0].strip()
        pos = nemo_icon_position.split()[1]
        data.append(pos + DAT_DELIMITER + entry)
    with io.open(get_dat_path(), "w") as f:
        f.write("\n".join(data))
    call(["notify-send", "Icon positions saved"])


def restore():
    desktop_dir = get_desktop_dir()
    for line in io.open(get_dat_path()):
        (pos, entry) = line.strip().split(DAT_DELIMITER)
        path = os.path.join(desktop_dir, entry)
        call([CMD_GVFS_SET_ATTRIBUTE, "-t", "string", path, ATTR_ICON_POSITION, pos])
    call(["notify-send", "Icon positions will be restored after relogin"])


def get_home_dir():
    return expanduser("~")


def get_desktop_dir():
    return check_output([CMD_XDG_USER_DIR, "DESKTOP"]).decode("utf-8").rstrip("\r\n")


def get_dat_path():
    return os.path.join(get_home_dir(), DAT_FILE)


def print_usage():
    print("Usage:\n  " + sys.argv[0] + " " + ACTION_SAVE + "\nor\n  " + sys.argv[0] + " " + ACTION_RESTORE)


DAT_FILE = ".desktop_alright"
DAT_DELIMITER = ">"
ACTION_SAVE = "save"
ACTION_RESTORE = "restore"
ATTR_ICON_POSITION = "metadata::nemo-icon-position"
CMD_XDG_USER_DIR = "xdg-user-dir"
CMD_GVFS_INFO = "gvfs-info"
CMD_GVFS_SET_ATTRIBUTE = "gvfs-set-attribute"


if __name__ == '__main__':
    main()
