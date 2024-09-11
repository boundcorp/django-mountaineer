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
            if "/test_" in controller_path:
                continue
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


def patch_enable_hotreload_controllers_in_views_folder():
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

class PageController(SyncControllerBase):
    def __init__(self, url: str | None = None, pages_dir="views/src/pages"):
        super().__init__()
        self.absolute_path = os.path.abspath(inspect.getabsfile(self.__class__))

        if not pages_dir in self.absolute_path:
            raise ValueError(f"PageController must be located in {pages_dir}")

        self.url = url or self.get_page_path(pages_dir)
        self.view_path = f"{self.get_relative_path(remove_leading_views=True)}/page.tsx"

    def get_page_path(self, pages_dir: str) -> str:
        remaining_path = self.get_relative_path().split(pages_dir)[-1]
        url = remaining_path or "/"
        if url.endswith("/index"):
            url = url[:-5]
        return url

    def get_relative_path(self, remove_leading_views: bool = False) -> str:
        parts = self.absolute_path.split("/")
        from_index = parts.index(
            "views"
        )  # find the first 'views' folder in the hierarchy
        if remove_leading_views:
            from_index += 1
        return "/".join(parts[from_index: -1])
