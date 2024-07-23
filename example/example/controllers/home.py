from datetime import datetime

from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase
from pydantic import BaseModel
from starlette.requests import Request

from example.auth import AuthDependencies


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime

    class Config:
        from_attributes = True


class UserOutput(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []
    user: UserOutput | None = None


class HomeController(ControllerBase):
    url = "/"
    view_path = "src/home/page.tsx"

    async def render(
            self,
            user: UserOutput | None = Depends(AuthDependencies.get_user),
    ) -> HomeRender:
        from example.apps.polls.models import Question

        return HomeRender(
            questions=[
                QuestionOutput.from_orm(question)
                async for question in Question.objects.all()
            ],
            user=user,
            metadata=Metadata(title="Home"),
        )
