# Simple Django-Mountaineer Integration Example

This is a simple example of how to integrate Django with [Mountaineer](https://mountaineer.sh).
These are the bare-minimum steps to get Django and Mountaineer to work together, which should be simple enough
to follow in any Django project. I've demonstrated this with a fresh Django project, to avoid unforeseen complications.

## Clean django and mountaineer projects

I started with a simplest-possible django project (called "backend") with a single app `polls`, following
the [Django tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/), and added a mountaineer project (
called "frontend").

```bash
django-admin startproject simpleintegration
cd simpleintegration
python manage.py startapp polls

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
rm -rf frontend/models frontend/views/app/detail frontend/views/app/home frontend/controllers/detail.py frontend/controllers/controller.py

# Append the Mountaineer .gitignore to your project root, this is important to ignore _server/ folders -
cat discard-outer-folder/.gitignore >>.gitignore

# Cleanup
rm -rf discard-outer-folder
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
You should view the [HomeController](/frontend/views/app/home/controller.py) at http://localhost:5006/,
which shows an example of retrieving resources from Django ORM and returning them via mountaineer SSR.

## Extras:

### PageController

I've also included a simple helper I wrote `PageController(url: string)` in
the [frontend/controller.py](/frontend/controller.py) file, which can be used to introspect the proper `page.tsx`;
it's totally optional, but I find it more convenient to colocate the page and controller logic within the
`frontend/views/` folder.

### Controller Sniffing

If you check my `frontend/app.py`, you'll see that I'm using a simple controller sniffing mechanism to automatically
load the controllers found within the `frontend/views` folder. This is a simple `django-ification` of the mountaineer
convention and just a personal preference.

### WIP
- [ ] use Django Auth in Mountaineer views

