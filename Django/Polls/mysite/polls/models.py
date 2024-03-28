"""
Models for the Polls application.
"""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Model representing a question.
    """
    question_text: str = models.CharField(max_length=200)
    pub_date: datetime.datetime = models.DateTimeField("date published")

    def __str__(self) -> str:
        """
        Returns the question text.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self) -> bool:
        """
        Checks if the question was published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Model representing a choice.
    """
    question: Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text: str = models.CharField(max_length=200)
    votes: int = models.IntegerField(default=0)

    def __str__(self) -> str:
        """
        Returns the choice text.
        """
        return self.choice_text
