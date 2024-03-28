"""
Views for the Polls application.
"""

from typing import Any
from django.db.models import F
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    """
    View for displaying a list of the latest questions.
    """
    template_name: str = "polls/index.html"
    context_object_name: str = "latest_question_list"

    def get_queryset(self) -> Any:
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    View for displaying details of a question.
    """
    model = Question
    template_name: str = "polls/detail.html"

    def get_queryset(self) -> Any:
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    View for displaying results of a question.
    """
    model = Question
    template_name: str = "polls/results.html"


def vote(request: HttpRequest, question_id: int) -> HttpResponseRedirect:
    """
    View for handling votes on a question.
    """
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
