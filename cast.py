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
from gi.repository import Nautilus, Gio, GObject, GConf


# Name of the gnome-shell extension
CAST_TO_TV = "cast-to-tv@rafostar.github.com"

# Path to the gnome-shell cast-to-tv extension
EXTENSION_PATH = os.path.expanduser(
    os.path.join("~/.local/share/gnome-shell/extensions", CAST_TO_TV))

UNSUPPORTED_TYPE = "image/svg+xml",

class CastExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        self.client = GConf.Client.get_default()

    def _get_chromecast_name(self):
        with open("/tmp/.cast-to-tv/config.json") as fp:
            config = json.load(fp)

            if config['receiverType'] != 'chromecast' or not config['chromecastName']:
                return

            with open(os.path.join(EXTENSION_PATH, 'devices.json')) as fp:
                for device in json.load(fp):
                    if device['name'] == config['chromecastName']:
                        return device['friendlyName']

    def _is_server_running(self):
        proc = subprocess.Popen(['pgrep', '-a', 'node'], stdout=subprocess.PIPE)

        for line in proc.stdout:
            if CAST_TO_TV in str(line):
                return True

        return False

    def _is_castable_media(self, file_obj):
        if file_obj.get_uri_scheme() != 'file':
            # Support for files under recent:// scheme
            if not file_obj.get_activation_uri().startswith('file://'):
                return False

        if file_obj.get_mime_type() in UNSUPPORTED_TYPE:
            return False

        return (file_obj.is_mime_type('audio/*') or 
            file_obj.is_mime_type('image/*') or
            file_obj.is_mime_type('video/*'))

    def _get_stream_type(self, file_obj):
        if file_obj.is_mime_type('video/*'):
            return "VIDEO"
        elif file_obj.is_mime_type('audio/*'):
            return "MUSIC"
        elif file_obj.is_mime_type('image/*'):
            return "PICTURE"

    def _start_server(self):
        server = os.path.join(EXTENSION_PATH, "node_scripts/server")
        subprocess.Popen(['/usr/bin/node', server])

    def _cast_files(self, selected_files):
        stream_type = self._get_stream_type(selected_files[0])

        # Make sure the playlist only contains the same media type
        playlist = [unquote(file_obj.get_activation_uri()[7:])
                    for file_obj in selected_files
                    if self._get_stream_type(file_obj) == stream_type]

        # Playlist must be updated before selection file
        with open("/tmp/.cast-to-tv/playlist.json", "w") as fp:
            json.dump(playlist, fp, indent=1)

        selection = {
            "streamType": stream_type,
            "subsPath": "",
            "filePath": playlist[0]
        }

        # The json file is monitored by the gnome-shell-extension
        # Whenever the file is touched, it will trigger a new cast session
        with open("/tmp/.cast-to-tv/selection.json", "w") as fp:
            json.dump(selection, fp, indent=1)

    def menu_activate_cb(self, menu, selected_files):
        self._cast_files(selected_files)

    def get_file_items(self, window, files):
        # Do not display menu if no temp files
        is_temp_access = (os.path.isfile("/tmp/.cast-to-tv/config.json") and
            os.path.isfile("/tmp/.cast-to-tv/playlist.json") and
            os.path.isfile("/tmp/.cast-to-tv/selection.json"))

        if not is_temp_access:
            return None

        selected_files = [file_obj for file_obj in files
                          if self._is_castable_media(file_obj)]

        if not selected_files:
            return None

        if not self._is_server_running():
            self._start_server()

        chromecast_name = self._get_chromecast_name()
        if chromecast_name:
            label = "Cast to {}".format(chromecast_name)
        else:
            label = "Cast Media"

        item = Nautilus.MenuItem(
            name='NautilusPython::cast_file_item',
            label=label)
        item.connect('activate', self.menu_activate_cb, selected_files)

        return item,

    def get_background_items(self, window, file):
        return None
