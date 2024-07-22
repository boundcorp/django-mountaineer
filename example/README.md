# Simple Django-Mountaineer Integration Example

This is a simple example of how to integrate Django with [Mountaineer](https://mountaineer.sh).
These are the bare-minimum steps to get Django and Mountaineer to work together, which you should be able
to follow in any Django project. I've demonstrated this with a fresh Django 5.0 project, to avoid unforeseen complications.

## Clean django and mountaineer projects

I started with a simplest-possible django project (`django-admin startproject backend`) with a single app `polls`,
following
the [Django tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/), and added a mountaineer project (
called "frontend").

## Mount Django in your Mountaineer app

Django can be mounted in a Mountaineer app by adding a few lines to the `frontend/app.py` file.

Add to `frontend/app.py` (mount django *after* mountaineer controller registrations):

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

You can start the normal Mountaineer development server with the following command:

```bash
poetry run runserver
```

While still using manage.py for most normal django functionality:

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

The django admin will be accessible at http://localhost:5006/admin/.
You should view the [HomeController](/frontend/controllers/home.py) at http://localhost:5006/,
which shows an example of retrieving resources from Django ORM and returning them via mountaineer SSR.

## Extras

### Controller Sniffing
If you check my `frontend/app.py`, you'll see that I'm using a simple controller sniffing mechanism to automatically
load the controllers files found within the `frontend/controllers` folder.
This is a simple django-esque autoloader to adapt to the mountaineer convention and just a personal preference.

### WIP

- [ ] use Django Auth in Mountaineer views