from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

import pickle
import re
import pandas as pd
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt

print (">> MODEL LOAD")
model = load_model("./models/best_model.keras")

print (">> LABEL LOAD")
with open("./models/tokenizer.pickle", "rb") as f:
    tokenizer = pickle.load(f)

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

@login_required(login_url='common:login')
def answer_create(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    if request.method=="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
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

def predict_sentence_positivity(sentence:str)->dict:
    okt = Okt()
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    max_len = 100
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(model.predict(pad_new)) # 예측
    result = (score > 0.5)
    prob = "{:.2f}".format(score * 100) if result else "{:.2f}".format((1 - score) * 100)
    is_positive = (1 if result else 0)
    return {"is_positive" : is_positive, "prob" : prob}