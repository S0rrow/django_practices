from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


