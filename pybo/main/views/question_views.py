from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='common:login')
def question_create(request):
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('main:index')
    else:
        form = QuestionForm()
    return render(request, 'main/question_form.html', {'form':form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "NOT AUTHORIZED TO EDIT")
        return redirect("main:detail", question_id = question.id)
    else:
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.modify_date = timezone.now()
                question.save()
                return redirect("main:detail", question_id=question.id)
        else:
            form = QuestionForm(instance=question)
   
    context = {'form' : form}
    return render(request, 'main/question_form.html',context )

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "NoAuthDeletion")
        return redirect("main:detail", question_id=question.id)
    else:
        question.delete()
        return redirect('main:index')