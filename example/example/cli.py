from click import command, option, group
from mountaineer.cli import handle_runserver, handle_watch, handle_build
from mountaineer.io import async_to_sync

from example.config import AppConfig


@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="example",
        webservice="example.main:app",
        webcontroller="example.app:app_controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="example",
        webcontroller="example.app:app_controller",
    )


@command()
def build():
    handle_build(
        webcontroller="example.app:app_controller",
    )
