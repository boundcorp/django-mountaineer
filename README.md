# Django-Mountaineer Integration 

Using Django with a FastAPI application like [Mountaineer](https://mountaineer.sh) is pretty straightforward, using FastAPI.mount().

However, there are a few gotchas in fully integrating Django, which this library aims to solve.

# Installation & Integration

You can reference the `example` folder for a complete example of a django project with a mountaineer app.

## Mount Django in your Mountaineer app (no library required)

Django can be mounted in a Mountaineer app by adding a few lines to the `example/app.py` file.

Add to `example/app.py` (mount django *after* mountaineer controller registrations):

```python
from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
import os

# These 2 lines will initialize django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django_app = get_asgi_application()

# Put these lines below your mountaineer controller.register() lines
controller.app.mount("/", django_app, name="app")
# This line is optional, but it mounts the static files from Django to the mountaineer app
# django normally uses /static for this, but this collides with mountaineer, so we should
# point django's STATIC_URL and STATIC_ROOT to /staticfiles
controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
```

## Run Django and Mountaineer together

You can start the normal Mountaineer development server with the following command, instead of django's runserver:
```bash
poetry run runserver
```

While still using manage.py for most normal django functionality:

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

The django admin will be accessible at http://localhost:5006/admin/.
You should view the [HomeController](/example/example/controllers/home.py) at http://localhost:5006/,
which shows an example of retrieving resources from Django ORM and returning them via mountaineer SSR.

## Extras

### Django Sessions and Authentication in FastAPI/Mountaineer

We have 2 options for exposing Django sessions and authentication in FastAPI/Mountaineer:

1. (heavy, more complete) Use django's full middleware stack, by adding the `django_mountaineer.DjangoMiddlewareRunner` to your FastAPI middleware.
2. (lightweight, less complete) Use `django_mountaineer.get_session` Dependency Injection, which is an async re-implementation of django's session middleware, for loading the user as a dependency.


### Controller Sniffing
If you check my `example/example/app.py`, you'll see that I'm using a simple controller sniffing mechanism to automatically
load the controllers files found within the `example/example/views` folder.
This is a simple django-esque autoloader to adapt to the mountaineer convention and just a personal preference.