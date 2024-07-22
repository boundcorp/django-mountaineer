from click import command, option
from mountaineer.cli import handle_runserver, handle_watch, handle_build

@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="frontend",
        webservice="frontend.main:app",
        webcontroller="frontend.app:app_controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="frontend",
        webcontroller="frontend.app:app_controller",
    )


@command()
def build():
    handle_build(
        webcontroller="frontend.app:app_controller",
    )

if __name__ == "__main__":
    runserver()