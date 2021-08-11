import subprocess
import sys
from pathlib import Path

import nox  # type: ignore

nox.options.reuse_existing_virtualenvs = True


@nox.session()
def run(session):
    session.install(".")
    session.run("python", "-m", "pyxtermjs", *session.posargs)


def has_changes():
    status = (
        subprocess.run(
            "git status --porcelain", shell=True, check=True, stdout=subprocess.PIPE
        )
        .stdout.decode()
        .strip()
    )
    return len(status) > 0


def on_master_no_changes(session):
    if has_changes():
        session.error("All changes must be committed or removed before publishing")
    # branch = get_branch()
    # if branch != "master":
    #     session.error(f"Must be on 'master' branch. Currently on {branch!r} branch")


def get_branch():
    return (
        subprocess.run(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )


@nox.session()
def build(session):
    session.install("--upgrade", "pip")
    session.install("build")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "-m", "build")


@nox.session()
def publish(session):
    on_master_no_changes(session)
    session.install("--upgrade", "pip")
    session.install("twine")
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
