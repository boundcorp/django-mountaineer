from django.db import models

class PublicChoices(models.TextChoices):
    PUBLIC = "public", "Public (everyone)"
    AUTHENTICATED = "authenticated", "Authenticated (logged in users)"
    PRIVATE = "emptya", "Private (only me)"

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publicity = models.CharField(max_length=200, choices=PublicChoices, default=PublicChoices.PUBLIC)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
