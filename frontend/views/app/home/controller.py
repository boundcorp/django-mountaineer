from datetime import datetime

from mountaineer import ControllerBase, Metadata, RenderBase
from pydantic import BaseModel

from frontend.controller import PageController


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime

    class Config:
        from_attributes = True


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []


class HomeController(PageController("/")):
    async def render(
            self,
    ) -> HomeRender:
        from backend.polls.models import Question

        return HomeRender(
            questions=[
                QuestionOutput.from_orm(question)
                async for question in Question.objects.all()
            ],
            metadata=Metadata(title="Home"),
        )
