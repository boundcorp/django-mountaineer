# DIY Simple Django-Mountaineer Integration Example

This is a simple example of how to integrate Django with [Mountaineer](https://mountaineer.sh).
These are the bare-minimum steps to get Django and Mountaineer to work together, which should be simple enough
to follow in any Django project. I've demonstrated this with a fresh Django project, to avoid unforeseen complications.

## Start with a  Django project

I started with a simplest-possible django project with a single app `polls`, following
the [Django tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/).

```bash
django-admin startproject simpleintegration
cd simpleintegration
python manage.py startapp polls
```

## Install [Mountaineer](https://mountaineer.sh)

Mountaineer provides a `create-mountaineer-project` helper that is quite comprehensive, but we only need a few of the
files it generates. I'll put it in a folder called `frontend/` for now, but you can choose anything you want here.

```bash
pipx run create-mountaineer-app
? Project name [my-project]: frontend
? Author [Leeward Bound <leeward@boundcorp.net>]
? Use poetry for dependency management? [Yes] Yes
? Create stub MVC files? [Yes] Yes
? Use Tailwind CSS? [Yes] Yes
? Add editor configuration? [vscode] no

Creating project...
```

Now we extract the necessary Mountaineer files, but remove all the SQLModel stuff.

```bash
# Take the inner frontend/ folder and move it to the root of the Django project
mv frontend/ discard-outer-folder/
mv discard-outer-folder/frontend/ .

# Remove the SQLModel stuff and references to Details and Home views in frontend
rm -rf frontend/models frontend/views/app/detail frontend/views/app/home frontend/controllers/detail.py frontend/controllers/home.py

# Append the Mountaineer .gitignore to your project root, this is important to ignore _server/ folders -
cat discard-outer-folder/.gitignore >>.gitignore

# Cleanup
rm -rf discard-outer-folder
```

Edit `frontend/config.py` and remove DatabaseConfig as a baseclass from AppConfig:

```python
from mountaineer import ConfigBase
class AppConfig(ConfigBase):
    pass
```

## Mount Django in your Mountaineer app

Django can be mounted in a Mountaineer app by adding a few lines to the `frontend/app.py` file.

Open your `frontend/app.py` and add the following lines:

```python
from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleintegration.settings')

django_app = get_asgi_application()

# Put these lines right after you initialize `controller = AppController()`
controller.app.mount("/staticfiles", StaticFiles(directory="staticfiles"), name="static")
controller.app.mount("/", django_app, name="app")
```

Finally, remove some references to SQLModel in `frontend/cli.py`:
```python
# Remove the models import
from frontend import models

...
# And remove the whole `createdb` function
@command()
@async_to_sync
async def createdb():
    _ = AppConfig() # type: ignore

    await handle_createdb(models)
```

## Run Django and Mountaineer together

You can start the normal Mountaineer development server with the following command:

```bash


