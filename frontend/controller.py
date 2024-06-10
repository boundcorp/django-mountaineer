import inspect
import os

from mountaineer import ControllerBase


def PageController(url: str):
    abs_path = os.path.abspath((inspect.stack()[1])[1]) # get the path of the file that called this function
    view_path = os.path.dirname(os.path.relpath(abs_path, start="everest/views"))
    typename = view_path.split("/")[-1].capitalize() + "Controller"
    return type(typename, (ControllerBase,), {
        "url": url,
        "view_path": f"{view_path}/page.tsx",
    })
