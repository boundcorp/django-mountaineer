import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from backend.urls import urlpatterns

django_app = get_asgi_application()

from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata
from django_mountaineer.controllers import register_controllers
from django_mountaineer.middleware import FastAPIDjangoMiddleware
from starlette.staticfiles import StaticFiles

from .config import AppConfig

config = AppConfig(find_controllers=["frontend/views", "backend/controllers"])

app_controller = AppController(
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
register_controllers(app_controller, config.find_controllers)

app_controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
app_controller.app.mount("/", django_app, name="app")

app_controller.app.add_middleware(FastAPIDjangoMiddleware, django_patterns=urlpatterns)
