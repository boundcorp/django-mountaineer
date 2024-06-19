import json

from asgiref.sync import sync_to_async
from django.contrib.auth import login, alogin
from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase, sideeffect, APIException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from frontend.auth import AuthDependencies

class FormError(APIException):
    status_code = 400
    detail = "An error occurred while processing the form"
    field_errors: dict[str, str] | None = None

class UserOutput(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class LoginRender(RenderBase):
    user: UserOutput | None = None


class LoginController(ControllerBase):
    url = "/login"
    view_path = "app/login/page.tsx"

    async def render(
            self,
            user: UserOutput | None = Depends(AuthDependencies.get_user),
    ) -> LoginRender:
        return LoginRender(
            user=user,
            metadata=Metadata(title="Login"),
        )

    @sideeffect(exception_models=[FormError])
    async def login(self, username: str, password: str, request: Request) -> None:

        if not username or not password:
            raise FormError(status_code=400, detail="Invalid username or password")

        from django.contrib.auth import authenticate
        user = await sync_to_async(authenticate)(username=username, password=password)
        if not user:
            raise FormError(status_code=400, detail="Invalid username or password")
        await alogin(request.state.django_request, user)
