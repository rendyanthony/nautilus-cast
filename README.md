# nautilus-cast
Cast video, music and pictures straight to your Chromecast from the comfort of your file manager. This Nautilus extension will add a Cast Media menu item to supported files in Nautilus.

## Requirements
* [gnome-shell-extension-cast-to-tv](https://github.com/Rafostar/gnome-shell-extension-cast-to-tv/)
* [nautilus-python](https://github.com/GNOME/nautilus-python/)

## Installation

After you install all the above dependencies:
```
curl https://raw.githubusercontent.com/rendyanthony/nautilus-cast/master/cast.py \
--create-dirs -o ~/.local/share/nautilus-python/extensions/cast.py
```

Last but not least, restart Nautilus:
```
nautilus -q
```
or:
```
killall nautilus
```

## How to use
1. Right click on a video, music or picture file in Nautilus.
1. Select Cast Media. 

## Special Thanks
Thanks to [@Rafostar](https://github.com/Rafostar) for the wonderful [Cast to TV](https://github.com/Rafostar/gnome-shell-extension-cast-to-tv/) Gnome Shell extension.
