from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    return render(
        request=request,
        template_name='main/question_list.html',
        context={'question_list' : page_obj}
    )

@login_required(login_url='common:login')
def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'main/question_detail.html', {'question':q})

def answer_create(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    if request.method=="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = q
            answer.save()
            return redirect('main:detail', question_id=q.id)
    else:
        form = AnswerForm()
    context = {"question":q, "form":form}
    return render(request, 'main/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('main:index')
    else:
        form = QuestionForm()
    return render(request, 'main/question_form.html', {'form':form})


