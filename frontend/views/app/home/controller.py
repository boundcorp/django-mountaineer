from datetime import datetime

from mountaineer import ControllerBase, Metadata, RenderBase
from pydantic import BaseModel


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime

    class Config:
        from_attributes = True


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

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
