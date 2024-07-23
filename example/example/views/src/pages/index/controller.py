from datetime import datetime
from inspect import getfile

from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase, LayoutControllerBase
from pydantic import BaseModel
from starlette.requests import Request

from example.auth import AuthDependencies
from django_mountaineer.controllers import PageController


class ChoiceOutput(BaseModel):
    choice_text: str
    votes: int
    class Config:
        from_attributes = True


class QuestionOutput(BaseModel):
    question_text: str
    pub_date: datetime
    choices: list[ChoiceOutput]

    class Config:
        from_attributes = True


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []


class HomeController(PageController()):
    async def render(
            self,
    ) -> HomeRender:
        from example.apps.polls.models import Question

        questions = Question.objects.prefetch_related('choices').all()
        return HomeRender(
            questions=[
                QuestionOutput(
                    question_text=question.question_text,
                    pub_date=question.pub_date,
                    choices=[
                        ChoiceOutput(choice_text=choice.choice_text, votes=choice.votes)
                        async for choice in question.choices.all()
                    ]
                )
                async for question in questions
            ],
            metadata=Metadata(title="Home"),
        )