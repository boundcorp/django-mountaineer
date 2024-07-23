from asgiref.sync import sync_to_async
from django.contrib.auth import alogin
from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase, sideeffect, APIException
from pydantic import BaseModel
from starlette.requests import Request

from example.auth import AuthDependencies, UserOutput

class FormError(APIException):
    status_code: int = 400
    detail: str = "An error occurred while processing the form"
    field_errors: dict[str, str] | None = None


class LoginRender(RenderBase):
    user: UserOutput | None = None


class LoginController(ControllerBase):
    url = "/login"
    view_path = "src/pages/login/page.tsx"

    def render(
            self,
    ) -> LoginRender:
        return LoginRender(
            metadata=Metadata(title="Login"),
        )

    @sideeffect
    async def login(self, username: str, password: str, request: Request):
        if not username or not password:
            raise FormError(status_code=400, detail="Invalid username or password")

        from django.contrib.auth import authenticate
        user = await sync_to_async(authenticate)(username=username, password=password)
        if not user:
            raise FormError(status_code=400, detail="Invalid username or password")
        await alogin(request.state.django_request, user)
        return LoginRender(
            user=user,
            metadata=Metadata(title="Login"),
        )
