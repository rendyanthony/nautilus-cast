# https://github.com/rendyanthony/nautilus-cast/
#
# Cast Media Nautilus extension
# Requires the Cast to TV Gnome Shell extension

import json
import os
import subprocess

# A way to get unquote working with python 2 and 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import gi
gi.require_version('GConf', '2.0')
from gi.repository import Nautilus, GObject, GConf


# Name of the gnome-shell extension
CAST_TO_TV = "cast-to-tv@rafostar.github.com"

# Path to the gnome-shell cast-to-tv extension
EXTENSION_PATH = os.path.expanduser(
    os.path.join("~/.local/share/gnome-shell/extensions", CAST_TO_TV))


class CastExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        self.client = GConf.Client.get_default()

    def _is_server_running(self):
        proc = subprocess.Popen(['pgrep', '-a', 'node'], stdout=subprocess.PIPE)

        for line in proc.stdout:
            if CAST_TO_TV in str(line):
                return True

        return False

    def _start_server(self):
        server = os.path.join(EXTENSION_PATH, "node_scripts/server")
        subprocess.Popen(['/usr/bin/node', server])

    def _cast_file(self, selected_file):
        stream_type = ""

        if selected_file.is_mime_type('video/*'):
            stream_type = "VIDEO"
        elif selected_file.is_mime_type('audio/*'):
            stream_type = "MUSIC"
        elif selected_file.is_mime_type('image/*'):
            stream_type = "PICTURE"
        else:
            return  #  Unable to determine the stream type

        file_path = unquote(selected_file.get_uri()[7:])

        playlist = [
            file_path
        ]

        # Playlist must be updated before selection file
        with open("/tmp/.cast-to-tv/playlist.json", "w") as fp:
            json.dump(playlist, fp, indent=1)

        selection = {
            "streamType": stream_type,
            "subsPath": "",
            "filePath": file_path
        }

        # The json file is monitored by the gnome-shell-extension
        # Whenever the file is touched, it will trigger a new cast session
        with open("/tmp/.cast-to-tv/selection.json", "w") as fp:
            json.dump(selection, fp, indent=1)

    def menu_activate_cb(self, menu, selected_file):
        self._cast_file(selected_file)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        selected_file = files[0]

        # Do not display menu if no temp files
        is_temp_access = (os.path.isfile("/tmp/.cast-to-tv/playlist.json") and
            os.path.isfile("/tmp/.cast-to-tv/selection.json"))

        if not is_temp_access:
            return None

        # Only display the menu for supported media
        is_castable_media = (selected_file.is_mime_type('audio/*') or
            selected_file.is_mime_type('image/*') or
            selected_file.is_mime_type('video/*'))

        if not is_castable_media:
            return None

        if not self._is_server_running():
            self._start_server()

        item = Nautilus.MenuItem(
            name='NautilusPython::cast_file_item',
            tip='Cast %s' % selected_file.get_name(),
            label='Cast Media')
        item.connect('activate', self.menu_activate_cb, selected_file)

        return item,

    def get_background_items(self, window, file):
        return None
