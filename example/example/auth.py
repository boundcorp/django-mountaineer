import time
from importlib import import_module

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model, load_backend
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.exceptions import SessionInterrupted
from django.utils.cache import cc_delim_re
from django.utils.crypto import constant_time_compare
from django.utils.http import http_date
from fastapi import Depends
from starlette.requests import Request
from starlette.responses import Response


SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
SESSION_KEY = "_auth_user_id"
BACKEND_SESSION_KEY = "_auth_user_backend"
HASH_SESSION_KEY = "_auth_user_hash"
REDIRECT_FIELD_NAME = "next"


def get_session(request: Request):
    session_key = request.cookies.get(settings.SESSION_COOKIE_NAME)
    return SessionStore(session_key)


class AuthDependencies():
    @staticmethod
    async def get_user(request: Request):
        from example.controllers.home import UserOutput
        if not hasattr(request.state, "django_request"):
            return None
        user = await request.state.django_request.auser()
        if user.is_anonymous:
            return None
        return UserOutput.from_orm(user)

    @staticmethod
    async def require_user(user=Depends(get_user)):
        if user.is_anonymous:
            raise Exception("User is not authenticated")
        return user


def get_user(request: Request, response: Response, session: SessionStore = Depends(get_session)):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from django.contrib.auth.models import AnonymousUser

    user = None
    try:
        user_id = get_user_model()._meta.pk.to_python(session[SESSION_KEY])
        backend_path = session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if hasattr(user, "get_session_auth_hash"):
                session_hash = session.get(HASH_SESSION_KEY)
                if not session_hash:
                    session_hash_verified = False
                else:
                    session_auth_hash = user.get_session_auth_hash()
                    session_hash_verified = constant_time_compare(
                        session_hash, session_auth_hash
                    )
                if not session_hash_verified:
                    # If the current secret does not verify the session, try
                    # with the fallback secrets and stop when a matching one is
                    # found.
                    if session_hash and any(
                            constant_time_compare(session_hash, fallback_auth_hash)
                            for fallback_auth_hash in user.get_session_auth_fallback_hash()
                    ):
                        session.cycle_key()
                        session[HASH_SESSION_KEY] = session_auth_hash
                    else:
                        session.flush()
                        user = None

    process_response(request, response, session)

    return user or AnonymousUser()


def patch_vary_headers(response, newheaders):
    """
    Add (or update) the "Vary" header in the given HttpResponse object.
    newheaders is a list of header names that should be in "Vary". If headers
    contains an asterisk, then "Vary" header will consist of a single asterisk
    '*'. Otherwise, existing headers in "Vary" aren't removed.
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if "Vary" in response.headers:
        vary_headers = cc_delim_re.split(response.headers["Vary"])
    else:
        vary_headers = []
    # Use .lower() here so we treat headers as case-insensitive.
    existing_headers = {header.lower() for header in vary_headers}
    additional_headers = [
        newheader
        for newheader in newheaders
        if newheader.lower() not in existing_headers
    ]
    vary_headers += additional_headers
    if "*" in vary_headers:
        response.headers["Vary"] = "*"
    else:
        response.headers["Vary"] = ", ".join(vary_headers)


def process_response(request, response, session):
    """
    If request.session was modified, or if the configuration is to save the
    session every time, save the changes and set a session cookie or delete
    the session cookie if the session has been emptied.
    """
    try:
        accessed = session.accessed
        modified = session.modified
        empty = session.is_empty()
    except AttributeError:
        return response
    # First check if we need to delete this cookie.
    # The session should be deleted only if the session is entirely empty.
    from django.conf import settings
    if settings.SESSION_COOKIE_NAME in request.cookies and empty:
        response.delete_cookie(
            settings.SESSION_COOKIE_NAME,
            path=settings.SESSION_COOKIE_PATH,
            domain=settings.SESSION_COOKIE_DOMAIN,
            samesite=settings.SESSION_COOKIE_SAMESITE,
        )
        patch_vary_headers(response, ("Cookie",))
    else:
        if accessed:
            patch_vary_headers(response, ("Cookie",))
        if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
            if session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = http_date(expires_time)
            # Save the session data and refresh the client cookie.
            # Skip session save for 5xx responses.
            if response.status_code < 500:
                try:
                    session.save()
                except UpdateError:
                    raise SessionInterrupted(
                        "The request's session was deleted before the "
                        "request completed. The user may have logged "
                        "out in a concurrent request, for example."
                    )
                response.set_cookie(
                    settings.SESSION_COOKIE_NAME,
                    session.session_key,
                    max_age=max_age,
                    expires=expires,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    path=settings.SESSION_COOKIE_PATH,
                    secure=settings.SESSION_COOKIE_SECURE or None,
                    httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
    return response
