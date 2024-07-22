from datetime import datetime

from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase
from pydantic import BaseModel
from starlette.requests import Request

from frontend.auth import AuthDependencies


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime


class UserOutput(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []
    user: UserOutput | None = None


class HomeController(ControllerBase):
    url = "/"
    view_path = "app/home/page.tsx"

    async def render(
            self,
            user: UserOutput | None = Depends(AuthDependencies.get_user),
    ) -> HomeRender:
        from backend.polls.models import Question

        return HomeRender(
            questions=[
                QuestionOutput.from_orm(question)
                async for question in Question.objects.all()
            ],
            user=user,
            metadata=Metadata(title="Home"),
        )
