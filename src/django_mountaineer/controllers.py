# Find all controllers in the specified directories
import glob
import os
from typing import List, Type

from mountaineer import ControllerBase


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
                    and not obj == ControllerBase
                ):
                    yield obj


def register_controllers(app_controller, search_paths):
    for controller in find_controllers(search_paths):
        app_controller.register(controller())
