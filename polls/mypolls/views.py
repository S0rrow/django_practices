from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
# Create your views here.

def index(request):
    latest_questions = Question.objects.all().order_by('-pub_date')[:5]
    context = {"latest_questions":latest_questions}
    return render(request, "mypolls/index.html", context)
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'mypolls/detail.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    select_choice = question.choice_set.get(pk=request.POST['choice'])
    select_choice.votes += 1
    select_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=[question.id]))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'mypolls/results.html', context)