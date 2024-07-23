from fastapi.staticfiles import StaticFiles
from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata
from django.core.asgi import get_asgi_application
import django
import os
from django_mountaineer.controllers import register_controllers
from django_mountaineer.middleware import FastAPIDjangoMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
django.setup()

from example.config import AppConfig

app_controller = AppController(
    config=AppConfig(), # type: ignore
    
    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],
    
)

django_app = get_asgi_application()

register_controllers(app_controller, ['example/controllers'])

app_controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
app_controller.app.mount("/", django_app, name="app")

from example.urls import urlpatterns

app_controller.app.add_middleware(FastAPIDjangoMiddleware, django_patterns=urlpatterns)
