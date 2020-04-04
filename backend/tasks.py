import os
import glob
from contextlib import contextmanager

from invoke import task, Collection
from fabric import Connection
from patchwork.transfers import rsync


def _build_backend(c):
    with c.cd("../frontend"):
        c.run("yarn build")


def _build_frontend(c):
    c.run("rm -rf dist")
    c.run("poetry build -f wheel")


@task
def build(c):
    _build_backend(c)
    _build_frontend(c)


@task
def load_context(c):
    if "url" not in c.server:
        c.server.url = input("Production SSH url:")
    if "remote_dir" not in c.server:
        c.server.remote_dir = input("Remote directory:")
    if "secret_key" not in c.server:
        c.server.remote_dir = input("Remote secret_key:")
    if "connection" not in c.server:
        c.server.connection = Connection(c.server["url"])


@task(pre=[load_context, build])
def release(c):
    server = c.server.connection
    wheel_path = glob.glob("dist/*.whl")[0]
    wheel_name = os.path.basename(wheel_path)
    remote_dir = c.server.remote_dir
    secret_key = c.server.secret_key
    with server.cd(remote_dir):
        server.put(wheel_path, remote=os.path.join(remote_dir, "backend", wheel_name))
        with server.cd("backend"):
            server.run("python3 -m virtualenv --clear .venv")
            server.run(f"echo \"export CORONASTATS_SECRET_KEY={secret_key}\" >> .venv/bin/activate")
            server.run(f"echo \"export FLASK_APP=coronastats:create_app\" >> .venv/bin/activate")
            with server.prefix("source .venv/bin/activate"):
                server.run(f"pip3 install {wheel_name}")
            server.run(f"rm {wheel_name}")
        server.run("rm -rf frontend/*")
    rsync(server, "../frontend/dist/*", os.path.join(remote_dir, "frontend"))
    server.put(
        "serverconfig/supervisor.conf",
        remote=os.path.join(remote_dir, "supervisor.conf"),
    )
    server.put(
        "serverconfig/nginx.conf", remote=os.path.join(remote_dir, "nginx.conf"),
    )


@task(pre=[load_context])
def upload_super(c):
    server = c.server.connection
    remote_dir = c.server.remote_dir
    server.put(
        "serverconfig/supervisor.conf",
        remote=os.path.join(remote_dir, "supervisor.conf"),
    )


ns = Collection(load_context, release, upload_super, build)
ns.configure({"server": {}})
