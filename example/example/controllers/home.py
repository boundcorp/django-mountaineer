from datetime import datetime

from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase, LayoutControllerBase
from pydantic import BaseModel
from starlette.requests import Request

from example.auth import AuthDependencies


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime

    class Config:
        from_attributes = True


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []


class HomeController(ControllerBase):
    url = "/"
    view_path = "src/pages/home/page.tsx"

    async def render(
            self,
    ) -> HomeRender:
        from example.apps.polls.models import Question

        return HomeRender(
            questions=[
                QuestionOutput.from_orm(question)
                async for question in Question.objects.all()
            ],
            metadata=Metadata(title="Home"),
        )