# pyxterm.js
A fully functional terminal in your browser.

![screenshot](https://github.com/cs01/pyxterm.js/raw/master/pyxtermjs.gif)

This is a Flask/socket.io websocket backend combined with the Xterm.js Javascript terminal emulator frontend. It works out of the box.

## Installation

### Option 1
This option installs system-wide or to your virtual environment. Should probably only be used if you're using a virtual environment.
```
pip install pyxtermjs
pyxtermjs  # run it from anywhere
```

### Option 2
This option installs system-wide and isolates all of pyxterm.js's dependencies, guaranteeing there are no dependency version conflicts. Requires [pipsi](https://github.com/mitsuhiko/pipsi) to be installed.
```
pipsi install pyxtermjs
pyxtermjs  # run it from anywhere
```

### Option 3
This option lets you play around with the source code. Requires [poetry](https://github.com/sdispater/poetry) to be installed.
```
git clone https://github.com/cs01/pyxterm.js.git
cd pyxterm.js
poetry install
python pyxtermjs/app.py
```
