import time
from importlib import import_module

from fastapi import Depends
from pydantic import BaseModel
from starlette.requests import Request


class UserOutput(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class AuthDependencies():
    @staticmethod
    async def get_user(request: Request):
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