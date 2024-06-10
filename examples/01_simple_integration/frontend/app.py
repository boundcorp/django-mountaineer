from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
import os
from mountaineer.app import AppController
from mountaineer.js_compiler.postcss import PostCSSBundler
from mountaineer.render import LinkAttribute, Metadata

from frontend.controllers.home import HomeController

from frontend.config import AppConfig

controller = AppController(
    config=AppConfig(),  # type: ignore

    global_metadata=Metadata(
        links=[LinkAttribute(rel="stylesheet", href="/static/app_main.css")]
    ),
    custom_builders=[
        PostCSSBundler(),
    ],

)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleintegration.settings')

django_app = get_asgi_application()

# Put these lines right after you initialize `controller = AppController()`
controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
controller.app.mount("/", django_app, name="app")

#controller.register(HomeController())
