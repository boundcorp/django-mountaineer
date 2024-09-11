from importlib import import_module

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse, StreamingResponse


class DjangoMiddlewareRunner:
    def __init__(self):
        self._load_middleware()

    def _load_middleware(self):
        self.middleware_stack = []
        from django.conf import settings

        for middleware_path in settings.MIDDLEWARE:
            middleware_module, middleware_classname = middleware_path.rsplit(".", 1)
            module = import_module(middleware_module)
            middleware_class = getattr(module, middleware_classname)
            middleware_instance = middleware_class(lambda r: r)
            self.middleware_stack.append(middleware_instance)

    def process_request(self, request: HttpRequest):
        for middleware in self.middleware_stack:
            if hasattr(middleware, "process_request"):
                response = middleware.process_request(request)
                if response:
                    return response
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse):
        for middleware in reversed(self.middleware_stack):
            if hasattr(middleware, "process_response"):
                response = middleware.process_response(request, response)
        return response


class FastAPIDjangoMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, django_patterns):
        super().__init__(app)
        self.django_middleware_runner = DjangoMiddlewareRunner()
        self.django_patterns = django_patterns

    async def dispatch(self, request: StarletteRequest, call_next):
        if [
            url
            for url in self.django_patterns
            if url.pattern.match(request.url.path.lstrip("/"))
        ]:
            return await call_next(request)
        django_request = await self.convert_to_django_request(request)
        response = self.django_middleware_runner.process_request(django_request)
        request.state.django_request = django_request
        if response is None:
            starlette_response = await call_next(request)
            if starlette_response is None:
                # Handle the case when no response is returned
                starlette_response = StarletteResponse(status_code=404, content="Not Found")
            django_response = await self.convert_to_django_response(starlette_response)
            django_response = await sync_to_async(
                self.django_middleware_runner.process_response
            )(django_request, django_response)
            return self.convert_to_starlette_response(django_response)
        else:
            return self.convert_to_starlette_response(response)

    async def convert_to_django_request(self, request: StarletteRequest) -> HttpRequest:
        django_request = HttpRequest()
        django_request.method = request.method
        django_request.path = request.url.path
        django_request.META = {
            "CONTENT_TYPE": request.headers.get("content-type", ""),
            "CONTENT_LENGTH": request.headers.get("content-length", ""),
            "HTTP_USER_AGENT": request.headers.get("user-agent", ""),
            "HTTP_COOKIE": request.headers.get("cookie", ""),
            "HTTP_AUTHORIZATION": request.headers.get("authorization", ""),
            "HTTP_X_CSRFTOKEN": request.headers.get(
                "x-csrftoken", request.cookies.get("csrftoken", "")
            ),
            # Include CSRF token header
            "QUERY_STRING": request.url.query,
            "SERVER_NAME": "localhost",  # Or the appropriate server name
            "SERVER_PORT": "8000",  # Or the appropriate server port
        }
        django_request.GET = request.query_params
        if request.method == "POST":
            django_request.POST = await request.form()
        else:
            django_request.POST = None
        django_request.COOKIES = request.cookies
        return django_request

    async def convert_to_django_response(
        self, response: StarletteResponse
    ) -> HttpResponse:
        if hasattr(response, "body_iterator"):
            content = b"".join([chunk async for chunk in response.body_iterator])
        else:
            content = response.body

        django_response = HttpResponse(
            content=content,
            status=response.status_code,
            content_type=response.media_type,
        )
        for header, value in response.headers.items():
            django_response[header] = value
        return django_response

    def convert_to_starlette_response(
        self, django_response: HttpResponse
    ) -> StarletteResponse:
        starlette_response = StarletteResponse(
            content=django_response.content,
            status_code=django_response.status_code,
            headers=dict(django_response.items()),
            media_type=django_response["Content-Type"],
        )
        for cookie in django_response.cookies.values():
            starlette_response.set_cookie(
                key=cookie.key,
                value=cookie.value,
                max_age=cookie["max-age"],
                expires=cookie["expires"],
                path=cookie["path"],
                domain=cookie["domain"],
                secure=cookie["secure"],
                httponly=cookie["httponly"],
                samesite=cookie["samesite"],
            )
        return starlette_response
