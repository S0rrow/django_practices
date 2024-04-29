from django.shortcuts import render
from django.urls import reverse
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
# Create your views here.

@api_view(['POST'])
def knn(request):
    with open('./restapi/knn_class_model.pkl.pk', 'rb') as f:
        knn_class_model = pickle.load(f)
    w = float(request.data.get('weight'))
    l = float(request.data.get('length'))
    data_arr = np.array([w,l])
    data_scaled = (data_arr - knn_class_model['mean'])/knn_class_model['std']
    if knn_class_model['model'].predict(data_scaled.reshape(1,2)).tolist()[0] == 0.0:
        return Response({"result":"빙어"})
    else: return Response({"result":"도미"})