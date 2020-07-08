#!/usr/bin/env python3
import argparse
from flask import Flask, render_template
from flask_socketio import SocketIO
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import shlex


__version__ = "0.4.0.1"

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.config["SECRET_KEY"] = "secret!"
app.config["fd"] = None
app.config["child_pid"] = None
socketio = SocketIO(app)


def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


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
    print("43: code here")
    from flask import request
    hostid = request.args.get('hostid', None)
    sessionid = request.args.get('sessionid', None)
    print("45: hostid: {}".format(hostid))
    print("45: sessionid: {}".format(sessionid))
    print("47: app.config: {}".format(app.config))
    app.config['hostid'] = hostid
    app.config['sessionid'] = sessionid
    return render_template("index.html")


@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    """write to the child pty. The pty sees this as if you are typing in a real
    terminal.
    """
    if app.config["fd"]:
        # print("writing to ptd: %s" % data["input"])
        os.write(app.config["fd"], data["input"].encode())


@socketio.on("resize", namespace="/pty")
def resize(data):
    if app.config["fd"]:
        set_winsize(app.config["fd"], data["rows"], data["cols"])


@socketio.on("connect", namespace="/pty")
def connect():
    """new client connected"""

    print("70: code here")
    #print("71: app.config: {}".format(app.config))
    print("71: sessionid: {}".format(app.config['sessionid']))
    print("71: hostid: {}".format(app.config['hostid']))

    if app.config["child_pid"]:
        # already started child process, don't start another
        return

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
        print("90: cmd: {}".format(cmd))
        print("92: app.config['cmd']: {}".format(app.config['cmd']))
        #cmd = "tlog-play -r es --es-baseurl=https://search-tlog-test-vthctr52ry4v2upvf2eyglhyfe.us-west-2.es.amazonaws.com/tlog-rsyslog/tlog/_search --es-query='session:3'"
        #cmd = 'tlog-play -r es --es-baseurl=https://search-tlog-test-vthctr52ry4v2upvf2eyglhyfe.us-west-2.es.amazonaws.com/tlog-rsyslog/tlog/_search --es-query=session:3'
        cmd = ['tlog-play', '-r', 'es', '--es-baseurl=https://search-tlog-test-vthctr52ry4v2upvf2eyglhyfe.us-west-2.es.amazonaws.com/tlog-rsyslog/tlog/_search', '--es-query=session:3']
        print("93: cmd: {}".format(cmd))
        #subprocess.run(app.config["cmd"])
        subprocess.run(cmd)
    else:
        # this is the parent process fork.
        # store child fd and pid
        app.config["fd"] = fd
        app.config["child_pid"] = child_pid
        set_winsize(fd, 50, 50)
        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
        print("99: cmd: {}".format(cmd))
        cmd = "tlog-play -r es --es-baseurl=https://search-tlog-test-vthctr52ry4v2upvf2eyglhyfe.us-west-2.es.amazonaws.com/tlog-rsyslog/tlog/_search --es-query='session:3'"
        print("101: cmd: {}".format(cmd))
        print("child pid is", child_pid)
        print(
            f"starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
        socketio.start_background_task(target=read_and_forward_pty_output)
        print("task started")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "A fully functional terminal in your browser. "
            "https://github.com/cs01/pyxterm.js"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--port", default=5000, help="port to run server on")
    parser.add_argument("--debug", action="store_true", help="debug the server")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument(
        "--command", default="bash", help="Command to run in the terminal"
    )
    parser.add_argument(
        "--cmd-args",
        default="",
        help="arguments to pass to command (i.e. --cmd-args='arg1 arg2 --flag')",
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)
    print(f"serving on http://127.0.0.1:{args.port}")
    app.config["cmd"] = [args.command] + shlex.split(args.cmd_args)
    #socketio.run(app, debug=args.debug, port=args.port)
    socketio.run(app, debug=args.debug, host='0.0.0.0', port=args.port)


if __name__ == "__main__":
    main()
