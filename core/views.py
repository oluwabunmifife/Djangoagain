from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

#For working with generic views
from django.views import generic


class IndexView(generic.ListView):
    template_name = "core/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        #Most recent 5 Questions posted
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "core/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "core/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "core/detail.html", {
            "question": question,
            "error_message": "You didn't select a Choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("core:results", args=(question_id,)))
    
#MANUALLY CODING THE VIEWS
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return render(request, "core/index.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "core/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "core/results.html", {"question": question})