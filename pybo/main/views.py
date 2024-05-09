from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
# Create your views here.

def index(request):
    question_list = Question.objects.order_by('-create_date')
    return render(
        request=request,
        template_name='main/question_list.html',
        context={'question_list' : question_list}
    )
    
def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'main/question_detail.html', {'question':q})

def answer_create(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    q.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('main:detail', question_id=q.id)