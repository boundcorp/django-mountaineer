import glob
import os

import django
from mountaineer import ControllerBase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from backend.urls import urlpatterns

django_app = get_asgi_application()

from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata
from starlette.staticfiles import StaticFiles

from frontend.config import AppConfig

config = AppConfig(find_controllers=["frontend/views", "frontend/controllers"])

controller = AppController(
    config=config,  # type: ignore

    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],

)

# This is the way we normally register controllers in mountaineer
# but we'll use the auto-discovery helper below, which is totally optional
# controller.register(HomeController())

# Find all controllers in the specified directories
for prefix in config.find_controllers:
    find_controllers = glob.glob(os.path.join(prefix, "**/*.py"), recursive=True)
    for controller_path in find_controllers:
        controller_module = controller_path.replace("/", ".").replace("\\", ".")[:-3]
        controller_module = __import__(controller_module, fromlist=[""])
        for name in dir(controller_module):
            obj = getattr(controller_module, name)
            if isinstance(obj, type) and issubclass(obj, ControllerBase) and not obj == ControllerBase:
                controller.register(obj())

controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
controller.app.mount("/", django_app, name="app")

from frontend.middleware import FastAPIDjangoMiddleware
controller.app.add_middleware(FastAPIDjangoMiddleware, django_patterns=urlpatterns)
