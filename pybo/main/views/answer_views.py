from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .model_views import predict_sentence_positivity


@login_required(login_url='common:login')
def answer_create(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    if request.method=="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = q
            result = predict_sentence_positivity(answer.content)
            answer.is_positive = result['is_positive']
            answer.probability = result['prob']
            answer.save()
            return redirect('main:detail', question_id=q.id)
    else:
        form = AnswerForm()
    context = {"question":q, "form":form}
    return render(request, 'main/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    a = get_object_or_404(Answer, pk=answer_id)
    if request.user != a.author:
        messages.error(request, "No Authority to modify this answer!")
        return redirect('main:detail', question_id=a.question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=a)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            result = predict_sentence_positivity(answer.content)
            answer.is_positive = result['is_positive']
            answer.probability = result['prob']
            answer.save()
            return redirect('main:detail', question_id=a.question.id)
    else:
        form = AnswerForm(instance=a)

    context = {'answer' : a, 'form' : form}
    return render(request, 'main/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    a = get_object_or_404(Answer, pk=answer_id)
    if request.user != a.author:
        messages.error(request, "No Authority to modify this answer!")
        return redirect('main:detail', question_id=a.question_id)
    else:
        a.delete()
    return redirect('main:detail', question_id=a.question_id)