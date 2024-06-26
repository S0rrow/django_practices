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