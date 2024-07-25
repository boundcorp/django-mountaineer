from datetime import datetime
from inspect import getfile
import time
from asgiref.sync import sync_to_async

from fastapi import Depends
from mountaineer import Metadata, RenderBase, ControllerBase, LayoutControllerBase, sideeffect
from pydantic import BaseModel, ConfigDict
from starlette.requests import Request
from django.db.models import F

from example.apps.polls.models import Choice, Question, PublicChoices
from django_mountaineer.controllers import PageController
from djantic import ModelSchema


class AsyncModelSchema(object):
    @classmethod
    def from_qs(cls, qs):
        return [cls.from_django(obj) for obj in qs]

    @classmethod
    async def afrom_qs(cls, qs):
        return [await sync_to_async(cls.from_django)(obj) async for obj in qs]
    

class ChoiceOutput(AsyncModelSchema, ModelSchema):
    model_config = ConfigDict(model=Choice)


class QuestionOutput(AsyncModelSchema, ModelSchema):
    model_config = ConfigDict(model=Question)
    choices: list[ChoiceOutput] = []
    publicity: PublicChoices

class CreateQuestion(BaseModel):
    question_text: str
    publicity: PublicChoices
    choices: list[str]


class HomeRender(RenderBase):
    questions: list[QuestionOutput] = []

# Need to wrap render in sync_to_async
class HomeController(PageController()):
    def render( self ) -> HomeRender:
        return HomeRender(
            questions=QuestionOutput.from_qs(Question.objects.prefetch_related('choices').all()),
            metadata=Metadata(title="Home"),
        )

    @sideeffect
    async def clear(self):
        await Question.objects.all().adelete()

    @sideeffect
    async def vote(self, question_id: int, choice_id: int) -> None:
        from example.apps.polls.models import Choice

        await Choice.objects.filter(id=choice_id, question_id=question_id).aupdate(votes=F('votes') + 1)


    @sideeffect
    async def create(self, data: CreateQuestion) -> None:
        from django.utils import timezone
        from example.apps.polls.models import Question, Choice

        question = await Question.objects.acreate(question_text=data.question_text, pub_date=timezone.now())
        for choice_text in data.choices:
            await Choice.objects.acreate(question=question, choice_text=choice_text)
