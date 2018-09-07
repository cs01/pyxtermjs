#!/usr/bin/env python3
import argparse
from flask import Flask, render_template
from flask_socketio import SocketIO
import pty
import os
import subprocess
import select

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.config["SECRET_KEY"] = "secret!"
app.config["fd"] = None
app.config["child_pid"] = None
socketio = SocketIO(app)


def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if app.config["fd"]:
            timeout_sec = 0
            (data_ready, _, _) = select.select([app.config["fd"]], [], [], timeout_sec)
            if data_ready:
                output = os.read(app.config["fd"], max_read_bytes).decode()
                socketio.emit("pty-output", {"output": output}, namespace="/pty")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    """write to the child pty"""
    if app.config["fd"]:
        os.write(app.config["fd"], data["input"].encode())


@socketio.on("connect", namespace="/pty")
def connect():
    """new client connected"""

    if app.config["child_pid"]:
        # already started child process, don't start another
        return

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run(["bash"])
    else:
        # this is the parent process fork.
        # store child fd and pid
        app.config["fd"] = fd
        app.config["child_pid"] = child_pid
        print("child pid is", child_pid)
        print(
            "starting background task to continously read and forward pty "
            "output to client"
        )
        socketio.start_background_task(target=read_and_forward_pty_output)
        print("task started")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    print(f"serving on http://127.0.0.1:{args.port}")
    socketio.run(app, debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
