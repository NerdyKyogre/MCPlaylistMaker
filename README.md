# MCPlaylistMaker
Python GUI to automatically create a Minecraft Java Edition resource pack which replaces the default music discs with sound files of the user's choice.

# Installation
Clone the repository using
```
git clone https://github.com/NerdyKyogre/MCPlaylistMaker
```
or download from the Releases page.

This program depends on tkinter and PIL, which can be installed with 
```
pip install tk pillow
```
before running.

# Usage
Open a terminal and navigate to the directory where the script is saved or cloned into.
Make sure that the program is executed in a directory that you have permission to write into, otherwise it will crash (i.e. right click and run in Windows does not work.)
Run
```
python playlistmaker.py
```
and follow the prompts.

**Note that only OGG and PNG files are supported, so make sure to convert in advance (I recommend ffmpeg or VLC for this).**

This script is theoretically cross-platform but as yet untested on Mac or certain linux environments, so you may encounter unexpected behaviour.

Enjoy!
