from click import command, option
from mountaineer.cli import handle_runserver, handle_watch, handle_build
import sys


@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="frontend",
        webservice="frontend.main:app",
        webcontroller="frontend.app:controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="frontend",
        webcontroller="frontend.app:controller",
    )


@command()
def build():
    handle_build(
        webcontroller="frontend.app:controller",
    )

if __name__ == "__main__":
    sys.exit(runserver())
