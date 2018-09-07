# pyxterm.js
A fully functional terminal in your browser.

![screenshot](https://github.com/cs01/pyxterm.js/raw/master/pyxtermjs.gif)

This is a Flask websocket backend combined with the Xterm.js Javascript terminal emulator in the frontend. It works out of the box and can run any application you want, including `bash`.

While useful on its own, the real purpose of this is to show a basic proof of concept on how to bring Xterm.js, Python, Flask, and Websockets together to make a useful tool.

It is a
* starting point to build your own web app with a terminal
* learning tool to understand what a `pty` is, and how to use one in Python
* way to see Flask and Flask-SocketIO in action
* way to play around with Xterm.js in a meaningful environment

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

## Documentation
```
>> pyxtermjs --help
usage: app.py [-h] [-p PORT] [--debug] [--command COMMAND]
              [--cmd-args CMD_ARGS]

A fully functional terminal in your browser.
https://github.com/cs01/pyxterm.js

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to run server on (default: 5000)
  --debug               debug the server (default: False)
  --command COMMAND     Command to run in the terminal (default: bash)
  --cmd-args CMD_ARGS   arguments to pass to command (i.e. --cmd-args='arg1
                        arg2 --flag') (default: )
```
