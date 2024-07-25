# Find all controllers in the specified directories
import glob
import inspect
import json
import os
from pathlib import Path
from typing import List, Type
from asgiref.sync import sync_to_async

from mountaineer import ControllerBase, LayoutControllerBase


def find_controllers(search_paths: List[str]) -> List[Type[ControllerBase]]:
    for prefix in search_paths:
        for controller_path in glob.glob(
            os.path.join(prefix, "**/*.py"), recursive=True
        ):
            controller_module = controller_path.replace("/", ".").replace("\\", ".")[
                :-3
            ]
            controller_module = __import__(controller_module, fromlist=[""])
            for name in dir(controller_module):
                obj = getattr(controller_module, name)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, ControllerBase)
                    and not obj in [ControllerBase, LayoutControllerBase]
                    and not inspect.isabstract(obj)
                ):
                    yield obj


def register_controllers(app_controller, search_paths):
    for controller in find_controllers(search_paths):
        app_controller.register(controller())


def enable_hotreload_controllers_in_views_folder():
    from mountaineer import cli

    def patched_is_view_update(path: Path):
        """
        mountaineer.cli defines is_view_update as `any(part == "views" for part in path.parts)`
        -- this includes all files in the views folder
        -- it is used to determine when a frontend-vs-backend hotreload is necessary
        -- we patch it here to exclude .py files in the views folder
        -- now .py files will trigger backend hotreload in the views/ directory
        """
        return any(part == "views" for part in path.parts) and not path.suffix == ".py"

    cli.is_view_update = patched_is_view_update


class SyncControllerBase(ControllerBase):
    """
    A base class for controllers that wraps render() in sync_to_async
    """

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        # wrap all functions in self in sync_to_async

        functions = list(self._get_client_functions())
        allow_names = ["render"] + [n for n, *_ in functions]

        for name in dir(self):
            func = getattr(self, name)
            if name not in allow_names or not callable(func):
                continue
            if not inspect.iscoroutinefunction(func):
                setattr(self, name, sync_to_async(func))

        return self


def PageController(url: str | None = None, page_path="src/pages"):
    abs_path = os.path.abspath(
        (inspect.stack()[1])[1]
    )  # get the path of the file that called this function
    parts = abs_path.split("/")
    views_index = parts.index("views")  # find the first 'views' folder in the hierarchy
    controller_path = "/".join(parts[views_index + 1 : -1])
    url = url or controller_path.split(page_path)[1] or "/"
    if url.endswith("/index"):
        url = url[:-5]
    return type(
        "PageController",
        (SyncControllerBase,),
        {
            "url": url,
            "view_path": f"{controller_path}/page.tsx",
        },
    )
