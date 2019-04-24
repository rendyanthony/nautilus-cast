# nautilus-cast
Cast video, music and pictures straight to your Chromecast from the comfort of your file manager. This Nautilus extension will add a Cast Media button to supported files in Nautilus.

# Requirements
* [gnome-shell-extension-cast-to-tv](https://github.com/Rafostar/gnome-shell-extension-cast-to-tv/)
* [nautilus-python](https://github.com/GNOME/nautilus-python/)

# Installation

Make sure you already have all the above dependencies.

Clone the latest source code:
```
git clone https://github.com/rendyanthony/nautilus-cast.git
```

Make sure the nautilus-python extensions directory is created:
```
mkdir -p ~/.local/share/nautilus-python/extensions/
```

Copy the Python script:
```
cp nautilus-cast/cast.py ~/.local/share/nautilus-python/extensions/
```

Last but not least, restart Nautilus.

# How to use
1. Right click on a video, music or picture file in Nautilus.
1. Select Cast Media. 

## Special Thanks
Thanks to [@Rafostar](https://github.com/Rafostar) the wonderful [Cast to TV](https://github.com/Rafostar/gnome-shell-extension-cast-to-tv/) Gnome Shell extension.