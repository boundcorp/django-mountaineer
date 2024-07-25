from click import command, option
from mountaineer.cli import handle_runserver, handle_watch, handle_build


from django_mountaineer.controllers import enable_hotreload_controllers_in_views_folder
enable_hotreload_controllers_in_views_folder()

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
